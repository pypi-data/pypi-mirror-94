from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.urls import NoReverseMatch, reverse

from admin_extra_urls.templatetags.extra_urls import get_preserved_filters

empty = object()


class Button:
    def __init__(self, path, *, label=None, icon='', permission=None,
                 css_class="btn btn-success", order=999, visible=empty, details=True, urls=None):
        self.path = path
        self.label = label or path

        self.icon = icon
        self._perm = permission
        self.order = order
        self.css_class = css_class
        self._visible = visible
        self._bound = False
        self.details = details
        self.urls = urls

    def bind(self, context):
        self.context = context
        obj = context.get('original', None)
        request = context['request']
        user = request.user
        self.querystring = get_preserved_filters(request)
        if callable(self._visible):
            self.visible = self._visible(obj)
        else:
            self.visible = self._visible

        if self._perm is None:
            self.authorized = True
        elif callable(self._perm):
            self.authorized = self._perm(request, obj)
        else:
            self.authorized = user.has_perm(self._perm)


class ButtonHREF(Button):

    def url(self):
        try:
            base_url = reverse(self.path)
        except NoReverseMatch:
            try:
                base_url = self.path.format(**self.context.flatten())
            except KeyError as e:
                base_url = str(e)
        self.label = base_url
        return "%s?%s" % (base_url, self.querystring)


class ChangeFormButton(ButtonHREF):
    details = True


class ChangeListButton(ButtonHREF):
    details = False


class ButtonAction(Button):
    def __init__(self, func, **kwargs):
        self.func = func
        super().__init__(**kwargs)
        self.path = self.path or func.__name__
        # self.label = self.label or labelize(func.__name__)
        self.method = func.__name__

    def url(self):
        opts = self.context['opts']
        if self.details:
            base_url = reverse(admin_urlname(opts, self.method),
                               args=[self.context['original'].pk])
        else:
            base_url = reverse(admin_urlname(opts, self.method))
        return "%s?%s" % (base_url, self.querystring)
