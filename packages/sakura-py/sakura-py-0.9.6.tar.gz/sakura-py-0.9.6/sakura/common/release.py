from gevent import Greenlet
from gevent.queue import Queue, Empty
from time import time
import weakref, atexit, gc, traceback

VERIFY_INTERVAL = 5
DEBUG = False

class AutoReleaseRegistry:
    def __init__(self):
        self.registry = {}
    def register_proxy(self, proxy, obj):
        ref = weakref.ref(proxy, self.release_object)
        self.registry[id(ref)] = (ref, obj)
    def release_object(self, r):
        ref, obj = self.registry[id(r)]
        del self.registry[id(r)]
        ReleaserGreenlet.schedule_release(obj)
    def force_release_all(self):
        for ref, obj in list(self.registry.values()):
            if DEBUG:
                print('force release', obj)
            if hasattr(obj, 'force_release'):
                obj.force_release()
            else:
                obj.release()
        self.registry = {}
        if DEBUG:
            print('done _force_release_all')
    def verify(self):
        if DEBUG:
            print('VERIFY')
        gc.collect()
        if DEBUG:
            for ref, obj in list(self.registry.values()):
                if getattr(obj, 'print_verify', False):
                    print(len(gc.get_referrers(ref())), obj)

REGISTRY = AutoReleaseRegistry()
atexit.register(REGISTRY.force_release_all)

class ReleaserGreenlet:
    instance = None
    def __init__(self):
        self.request_queue = Queue()
    @staticmethod
    def schedule_release(obj):
        if ReleaserGreenlet.instance is None:
            ReleaserGreenlet.instance = ReleaserGreenlet()
            ReleaserGreenlet.instance.spawn()
        ReleaserGreenlet.instance.request_queue.put(obj)
    def run(self):
        verify_time = time() + VERIFY_INTERVAL
        try:
            while True:
                timeout = verify_time - time()
                if timeout <= 0:
                    timeout = 0.01
                obj = None
                try:
                    obj = self.request_queue.get(block=True, timeout=timeout)
                except Empty:
                    pass
                if obj is not None:
                    obj_s = str(obj)
                    if DEBUG:
                        print("releaser: now releasing", obj_s)
                    obj.release()
                    if DEBUG:
                        print("releaser:", obj_s, "released")
                if time() > verify_time:
                    REGISTRY.verify()
                    verify_time = time() + VERIFY_INTERVAL
        except:
            print('Exception in Releaser Greenlet:')
            traceback.print_exc()
    def spawn(self):
        return Greenlet.spawn(self.run)

class AutoReleaseProxy:
    Registry = {}
    def __init__(self, obj):
        self.obj = obj
        REGISTRY.register_proxy(self, obj)
    # redirect everything to self.obj
    def __getattr__(self, attr):
        return getattr(self.obj, attr)
    def __iter__(self):
        it = iter(self.obj)
        if it is self.obj:
            return self
        return it
    def __str__(self):
        return 'proxy<' + str(self.obj) + '>'
    def __repr__(self):
        return 'proxy<' + repr(self.obj) + '>'
    def __next__(self):
        return next(self.obj)
    def __enter__(self):
        o = self.obj.__enter__()
        if o is self.obj:
            return self
        return o
    def __exit__(self, *args):
        self.obj.__exit__(*args)

def auto_release(cls):
    class ARClass:
        def __call__(self, *args, **kwargs):
            inst = cls(*args, **kwargs)
            return AutoReleaseProxy(inst)
        def __getattr__(self, attr):
            return getattr(cls, attr)
    return ARClass()
