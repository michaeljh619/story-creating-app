ROUTES = {

"addStoryPage_route": '/categories/<int:category_id>/story/<int:story_id>/page/add/<int:linking_page_id>',

"authorized_route": "/authorized",

"deleteStoryPage_route": "/categories/<int:category_id>/story/<int:story_id>/page/delete/<int:page_id>",

"deleteStory_route": '/categories/<int:category_id>/story/<int:story_id>/delete',

"editStoryPage_route": "/categories/<int:category_id>/story/<int:story_id>/page/edit/<int:page_id>",

"editPages_route": '/categories/<int:category_id>/story/<int:story_id>/pages',

"editStory_route": '/categories/<int:category_id>/story/<int:story_id>/edit',

"showHome_route": '/',

"login_route": '/login',

"logout_route": '/logout',

"newStory_route": '/categories/story/new',

"showProfile_route": '/profile',

"showCategories_route": '/categories/',

"showCategoriesJSON_route": '/categories/json',

"showCategory_route": '/categories/<int:category_id>/',

"showCategoryJSON_route": '/categories/<int:category_id>/json',

"showPageJSON_route": '/categories/<int:category_id>/story/<int:story_id>/page/<int:page_id>/json',

"showStory_route": '/categories/<int:category_id>/story/<int:story_id>/page/<int:page_id>',

"showStoryJSON_route": '/categories/<int:category_id>/story/<int:story_id>/json'

}
