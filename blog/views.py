from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Comment
import json
from django.core.paginator import Paginator
from .models import Post, Comment, Like
from django.http import HttpResponse


# ======================
# (A) AUTHENTICATION
# ======================
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            return JsonResponse({'success': f'User {user.username} created'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            login(request, user)
            return JsonResponse({'success': 'Logged in'})
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)

# ======================
# (B) POSTS & COMMENTS
# ======================
@csrf_exempt
def create_post(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post = Post.objects.create(
                author=request.user,
                title=data['title'],
                content=data['content']
            )
            return JsonResponse({'id': post.id, 'title': post.title}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)

def edit_post(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)
    
    try:
        post = Post.objects.get(id=post_id, author=request.user)
        if request.method == 'POST':
            data = json.loads(request.body)
            post.title = data.get('title', post.title)
            post.content = data.get('content', post.content)
            post.save()
            return JsonResponse({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'message': 'Post updated successfully'
            })
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found or unauthorized'}, status=404)

def delete_post(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)
    
    try:
        post = Post.objects.get(id=post_id, author=request.user)  # Only author can delete
        post.delete()
        return JsonResponse({'success': 'Post deleted'})
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found or unauthorized'}, status=404)

def list_posts(request):
    page_number = request.GET.get('page', 1)  # Get page number from URL (e.g., /api/posts/?page=2)
    posts = Post.objects.all().values('id', 'title', 'author__username', 'created_at')
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_obj = paginator.get_page(page_number)
    return JsonResponse({
        'posts': list(page_obj.object_list),  # Current page posts
        'has_next': page_obj.has_next(),      # Is there a next page?
        'current_page': page_obj.number       # Current page number
    })

def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post).values('id', 'user__username', 'text', 'created_at')
        return JsonResponse({
            'post': {
                'title': post.title,
                'content': post.content,
                'author': post.author.username,
                'created_at': post.created_at,
            },
            'comments': list(comments)
        })
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

@csrf_exempt
def add_comment(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post = Post.objects.get(id=post_id)
            comment = Comment.objects.create(
                post=post,
                user=request.user,
                text=data['text']
            )
            return JsonResponse({'success': 'Comment added'}, status=201)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)

@csrf_exempt
def like_post(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)
    
    try:
        post = Post.objects.get(id=post_id)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            return JsonResponse({'success': 'Like removed'})
        return JsonResponse({'success': 'Post liked'})
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    
def home(request):
    return HttpResponse("""
    <h1>Welcome to Blog API</h1>
    <p>Available endpoints:</p>
    <ul>
        <li><a href="/api/register/">/api/register/</a> - User registration</li>
        <li><a href="/api/login/">/api/login/</a> - User login</li>
        <li><a href="/api/posts/">/api/posts/</a> - List all posts</li>
    </ul>
    """)