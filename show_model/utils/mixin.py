from django.contrib.auth.decorators import login_required

class Loginrequiremixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        #调用父类的as-view
        view = super(Loginrequiremixin, cls).as_view(**initkwargs)
        return login_required(view)


