from django.conf.urls import patterns, url

urlpatterns = patterns('gnowsys_ndf.ndf.views.forum',
                       url(r'^(?P<node_id>[\w-]+)$', 'forum', name='forum'),
                       url(r'^create/$', 'create_forum', name='create_forum'),
                       url(r'^show/(?P<forum_id>[\w-]+)$', 'display_forum', name='show'),
                       url(r'^thread/(?P<thread_id>[\w-]+)$', 'display_thread', name='thread'),

                       url(r'^add_node/$','add_node',name="add_node"),
)

