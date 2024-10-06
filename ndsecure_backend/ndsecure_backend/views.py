from django.http import HttpResponse

def home(request):
    return HttpResponse("""
    <h1>Welcome to NDSecure</h1>
    <p>This is a secure note-sharing application.</p>
    <ul>
        <li><a href="/admin/">Admin Interface</a></li>
        <li><a href="/api/notes/">API: List/Create Notes</a></li>
    </ul>
    """)