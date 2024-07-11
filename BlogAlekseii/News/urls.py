from django.urls import path
from .views import (
    NewsListView,
    NewsDetailCategory,
    NewsDetailTag,
    NewsDetailView,
    share_facebook,
    share_twitter,
    share_linkedin,
    share_pinterest,
    SearchResultsView,
    FeedbackCreateView,
    contact_thanks_view,
    rss_feed
)

urlpatterns = [
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('', NewsListView.as_view(), name='news_list'),
    path('rss/', rss_feed, name='rss_feed'),
    path('<slug:category_slug>/', NewsDetailCategory.as_view(), name='news_category'),
    path('tag/<slug:tag_slug>/', NewsDetailTag.as_view(), name='news_tag_detail'),
    path('<slug:category_slug>/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
    path('share/facebook/', share_facebook, name='share_facebook'),
    path('share/twitter/', share_twitter, name='share_twitter'),
    path('share/twitter/', share_twitter, name='share_twitter'),
    path('share/linkedin/', share_linkedin, name='share_linkedin'),
    path('share/pinterest/', share_pinterest, name='share_pinterest'),
    path('/feedback/', FeedbackCreateView, name='feedback'),
    path('/feedback/thanks/', contact_thanks_view, name='forms_home_thanks'),
]
