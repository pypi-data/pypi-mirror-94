from sakura.hub.context import get_context
from sakura.hub.mixins.bases import BaseMixin
from sakura.common.errors import APIOperatorError
from gevent.lock import Semaphore

class OpInstanceMixin(BaseMixin):
    INSTANCIATED = set()
    MOVING = set()
    DELETING = set()
    RELOAD_NOT_COMPLETED = set()
    LOCAL_STREAMS = {}
    LOCKS = {}
    INFO_CACHE = {}
    def __str__(self):
        return '%s op_id=%d' % (self.op_class.metadata['name'], self.id)
    def discard_info_cache(self):
        if self.id in OpInstanceMixin.INFO_CACHE:
            del OpInstanceMixin.INFO_CACHE[self.id]
    def set_gui_data(self, gui_data):
        self.gui_data = gui_data
        self.discard_info_cache()
    @property
    def daemon_api(self):
        return self.daemon.api
    @property
    def remote_instance(self):
        # note: the following shortcut will become valid only after
        # the operator has been instanciated with function
        # reload_on_daemon() below.
        return self.daemon_api.op_instances[self.id]
    @property
    def enabled(self):
        return self.id in OpInstanceMixin.INSTANCIATED
    @enabled.setter
    def enabled(self, boolean):
        if boolean:
            if not self.enabled:
                self.push_event('enabled')
                OpInstanceMixin.INSTANCIATED.add(self.id)
                self.discard_info_cache()
        else:
            if self.enabled:
                self.push_event('disabled')
                OpInstanceMixin.INSTANCIATED.discard(self.id)
                self.discard_info_cache()
    @property
    def lock(self):
        op_lock = OpInstanceMixin.LOCKS.get(self.id, None)
        if op_lock is None:
            op_lock = Semaphore()
            OpInstanceMixin.LOCKS[self.id] = op_lock
        return op_lock
    @property
    def moving(self):
        return self.id in OpInstanceMixin.MOVING
    @moving.setter
    def moving(self, boolean):
        if boolean:
            OpInstanceMixin.MOVING.add(self.id)
        else:
            OpInstanceMixin.MOVING.discard(self.id)
    @property
    def deleting(self):
        return self.id in OpInstanceMixin.DELETING
    @deleting.setter
    def deleting(self, boolean):
        if boolean:
            OpInstanceMixin.DELETING.add(self.id)
        else:
            OpInstanceMixin.DELETING.discard(self.id)
    def push_event(self, *args, **kwargs):
        # do not push events to GUI when moving or deleting
        if not self.moving and not self.deleting:
            super().push_event(*args, **kwargs)
    @property
    def disabled_message(self):
        if self.op_class.enabled:
            if self.id in OpInstanceMixin.RELOAD_NOT_COMPLETED:
                return 'Latest code changes prevented this operator to load properly.'
            else:
                return 'Daemon running this operator was just stopped.'
        else:
            return self.op_class.disabled_message
    @property
    def local_streams(self):
        return OpInstanceMixin.LOCAL_STREAMS.get(self.id)
    @local_streams.setter
    def local_streams(self, streams):
        OpInstanceMixin.LOCAL_STREAMS[self.id] = streams
    def aggregate_events(self, events):
        final_status_event = None
        for event in events:
            assert event is not None, "Got 'None' event!"
            if (final_status_event, event) == (None, 'enabled'):
                final_status_event = 'enabled'
            elif (final_status_event, event) == (None, 'disabled'):
                final_status_event = 'disabled'
            elif (final_status_event, event) == ('enabled', 'disabled'):
                final_status_event = None
            elif (final_status_event, event) == ('disabled', 'enabled'):
                final_status_event = None
            else:
                assert final_status_event != event, "Got repeated operator event: " + event
        if final_status_event is None:
            # remove 'enabled' and 'disabled' from list
            events = list(event for event in events if event not in ('enabled', 'disabled'))
        else:
            # only keep the last status event
            rev_events = []
            found = False
            for event in reversed(events):
                if event in ('enabled', 'disabled'):
                    if found:
                        continue    # discard
                    if event != final_status_event:
                        continue    # discard
                    # found last status event
                    found = True
                rev_events.append(event)
            events = list(reversed(rev_events))
        # remove duplicated events (keep last occurence)
        rev_events = []
        for event in reversed(events):
            if event not in rev_events:
                rev_events.append(event)
        events = list(reversed(rev_events))
        return events
    def __getattr__(self, attr):
        # find other attributes at the real operator
        # instance on the daemon side.
        if attr != 'warning_message' and not 'internal' in attr:
            return getattr(self.remote_instance, attr)
        raise AttributeError

    def iterate_all_ops_of_cls(self):
        """Iterates over all operators of this class the current user has."""
        for op in self.op_class.op_instances:
            if op.dataflow.owner == self.dataflow.owner:
                yield op

    @property
    def num_ops_of_cls(self):
        """Indicates how many instances of this class the user has."""
        return len(tuple(self.iterate_all_ops_of_cls()))

    def pack_repo_info(self, **flags):
        info = self.op_class.pack_repo_info(revision_prefix='', **flags)
        if info['repo_type'] == 'git':
            info.update(
                code_ref = self.revision['code_ref'],
                commit_hash = self.revision['commit_hash']
            )
        return info

    def pack(self):
        with self.lock:
            res = OpInstanceMixin.INFO_CACHE.get(self.id)
            if res is None:
                res = dict(
                    op_id = self.id,
                    cls_id = self.op_class.id,
                    cls_name = self.op_class.metadata['name'],
                    gui_data = self.gui_data,
                    num_ops_of_cls = self.num_ops_of_cls,
                    **self.pack_repo_info(),
                    **self.pack_status_info()
                )
                if self.enabled:
                   res.update(**self.remote_instance.pack())
                OpInstanceMixin.INFO_CACHE[self.id] = res
                print('info cache for instance', self.id, 'refreshed')
        return res

    @property
    def sorted_params(self):
        # sort params according to param_id
        yield from sorted(self.params, key=lambda param: param.param_id)

    def recheck_params(self):
        # recheck params in order
        for param in self.sorted_params:
            param.recheck()

    def update_revision(self, code_ref, commit_hash, all_ops_of_cls=False):
        if all_ops_of_cls:
            ops = self.iterate_all_ops_of_cls()
        else:
            ops = [ self ]
        for op in ops:
            old_revision = op.revision
            op.revision = dict(code_ref = code_ref, commit_hash = commit_hash)
            try:
                op.reload()
                op.discard_info_cache()
            except:
                # failed, restore
                op.revision = old_revision
                op.reload()
                raise

    def resync_params(self):
        # resync number of parameters with what the daemon reports (possible source code change)
        local_ids = set(param.param_id for param in self.params)
        remote_ids = set(range(self.remote_instance.get_num_parameters()))
        for param in self.params:
            if param.param_id not in remote_ids:
                param.delete()
        context = get_context()
        for param_id in (remote_ids - local_ids):
            param = context.op_params(op = self, param_id = param_id) # instanciate in local db
            context.db.commit()
        # setup parameters with remote daemon
        for param in self.sorted_params:
            param.setup()
    def delete_on_daemon(self):
        self.enabled = False
        self.daemon_api.delete_operator_instance(self.id)
        self.discard_info_cache()
    def disable_links(self):
        for link in self.downlinks:
            link.deinstanciate()
        for link in self.uplinks:
            link.deinstanciate()
        self.discard_info_cache()
    def reload(self):
        if self.enabled:
            OpInstanceMixin.RELOAD_NOT_COMPLETED.add(self.id)
            self.disable_links()
        self.reload_on_daemon()
        OpInstanceMixin.RELOAD_NOT_COMPLETED.discard(self.id)
        # a source code change may cause invalid links
        # we cannot simply disable them, we have to delete them
        remote_info = self.remote_instance.pack()
        for link in tuple(self.uplinks):
            if link.dst_in_id >= len(remote_info['inputs']):
                print('dropped input link, no longer valid')
                link.delete_link()
        for link in tuple(self.downlinks):
            if link.src_out_id >= len(remote_info['outputs']):
                print('dropped output link, no longer valid')
                link.delete_link()
        self.resync_params()
        self.restore_links()
        self.discard_info_cache()
    def reload_on_daemon(self):
        if not self.enabled:
            # not running yet, create it on daemon
            self.daemon_api.create_operator_instance(
                self.id,
                event_recorder = self.on_daemon_events,
                local_streams = self.local_streams,
                **self.pack_repo_info(include_sandbox_attrs=True)
            )
        else:
            # already running on daemon, reload it
            self.enabled = False
            self.daemon_api.reload_operator_instance(
                self.id,
                event_recorder = self.on_daemon_events,
                local_streams = self.local_streams,
                **self.pack_repo_info(include_sandbox_attrs=True)
            )
        self.enabled = True
        self.discard_info_cache()
    def on_daemon_events(self, evts):
        self.discard_info_cache()
        for evt in evts:
            evt_name, evt_args, evt_kwargs = evt
            if evt_name in ('hub:input_now_none', 'hub:input_no_longer_none'):
                # translate these events to a callback on the
                # appropriate link object.
                dst_in_id = evt_args[0]
                link = None
                for link in tuple(self.uplinks):
                    if link.dst_in_id == dst_in_id:
                        break
                # if event was caused by link deletion, we might
                # not find it!
                if link is not None:
                    link.on_daemon_event(evt_name)
            elif evt_name == 'hub:check_move':
                self.check_move()
            else:
                self.push_event(evt_name, *evt_args, **evt_kwargs)    # just push other events to UI
    def on_daemon_disconnect(self):
        self.discard_info_cache()
        # daemon stopped
        self.disable_links()
        self.enabled = False
    def ready(self):
        if not self.enabled:
            return False
        for link in self.uplinks:
            if not link.enabled:
                return False
        for param in self.params:
            if not param.is_valid:
                return False
        return True
    @classmethod
    def create_instance(cls, dataflow, op_cls_id,
                local_streams = None, gui_data = '', **revision_kwargs):
        context = get_context()
        # create in local db
        op = cls(daemon = None, dataflow = dataflow, op_class = op_cls_id,
                                gui_data = gui_data, **revision_kwargs)
        # refresh op id
        context.db.commit()
        op.local_streams = local_streams
        with op.lock:
            # run on an appropriate daemon
            try:
                op.move()
            except:
                op.delete()
                raise
            # auto-set params when possible
            op.recheck_params()
            # notify event listeners
            dataflow.push_event('created_instance', op.id)
        return op.id
    def delete_instance(self):
        self.deleting = True
        self.disable_links()
        # remove 1-hop links (since these are connected to
        # the operator instance we are removing)
        for link in self.uplinks:
            link.delete_link()
        for link in self.downlinks:
            link.delete_link()
        # delete instance remotely
        if self.enabled:
            self.delete_on_daemon()
        self.deleting = False   # done
        # notify event listeners
        self.dataflow.push_event('deleted_instance', self.id)
        # delete instance in local db
        self.delete()
        get_context().db.commit()
    def check_move(self):
        if self.moving:     # discard if already moving
            return
        with self.lock:
            self.move()
    def move(self):
        # list available daemons, current first
        # (if self.daemon already has a value)
        daemons = sorted(get_context().daemons.all_enabled(),
                         key = lambda daemon: daemon != self.daemon)
        if len(daemons) == 0:
            raise APIOperatorError("No daemon is available")
        self.moving = True
        if self.op_class.has_custom_affinity():
            affinities = self.custom_daemon_affinities(daemons)
        else:
            affinities = self.default_daemon_affinities(daemons)
        # check that we can move somewhere
        if len(affinities) == 0:
            self.moving = False
            raise APIOperatorError('This operator is not compatible with available daemons!')
        # check best affinity
        best = (None, -1)
        for daemon in daemons:
            score = affinities[daemon]
            if score > best[1]:
                best = (daemon, score)
        # migrate to best match
        if self.daemon is None or affinities[self.daemon] < best[1]:
            self.discard_info_cache()
            print('MOVE', self, self.daemon, '->', best[0])
            daemon = best[0]
            self.move_out()
            self.move_in(daemon)
            print('MOVE END', self)
        # ok done
        self.moving = False
    def move_out(self):
        if self.enabled:
            # disable links
            self.disable_links()
            # drop op
            self.delete_on_daemon()
    def move_in(self, daemon):
        # associate
        self.daemon = daemon
        # recreate op
        self.restore()
    def get_ouputplug_link_id(self, out_id):
        for l in self.downlinks:
            if l.src_out_id == out_id:
                return l.id
        return None     # not connected
    def restore_links(self):
        self.discard_info_cache()
        # restore uplinks if src daemon is ok
        for link in self.uplinks:
            if link.src_op.enabled:
                link.instanciate()
        # restore downlinks if dst daemon is ok
        for link in self.downlinks:
            if link.dst_op.enabled:
                link.instanciate()
    def restore(self):
        self.discard_info_cache()
        self.reload_on_daemon()
        self.resync_params()
        self.restore_links()
    def default_daemon_affinities(self, daemons):
        daemon_info = { daemon.get_origin_id(): daemon for daemon in daemons }
        affinity_points = { origin_id: 0 for origin_id in daemon_info.keys() }
        # if the operator is just being instanciated, then it probably has no
        # input or output source ready, so return affinity 0 for all daemons.
        if self.enabled:
            inputs_origins, outputs_origins = self.get_plug_origins()
            # add 3 points per input source on a given daemon
            for origin_id in inputs_origins:
                if origin_id is not None:
                    affinity_points[origin_id] += 3
            # add 1 point per output source on a given daemon
            for origin_id in outputs_origins:
                if origin_id is not None:
                    affinity_points[origin_id] += 1
        return { daemon_info[origin_id]: points \
                for origin_id, points in affinity_points.items() }
    def custom_daemon_affinities(self, daemons):
        affinities = {}
        # try available daemons
        for daemon in daemons:
            if daemon != self.daemon:   # if not already current
                self.move_out()
                try:
                    self.move_in(daemon)
                except: # not compatible
                    continue
            affinities[daemon] = self.env_affinity()
        return affinities
    def sync_handle_event(self, *args, **kwargs):
        with self.lock:
            return self.remote_instance.sync_handle_event(*args, **kwargs)
