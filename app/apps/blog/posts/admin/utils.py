from ..models import BlogPost

def with_post(fun, *args, **kwargs):
    def decorate(self, post_id=None):
        post = None
        if post_id:
            post = BlogPost.get_by_id(int(post_id))
            if not post:
                self.error(404)
                return

        return fun(self, post, *args, **kwargs)
    return decorate