// Handle logout
function logout() {
    fetch('/logout', {
        method: 'POST',
        credentials: 'same-origin'
    })
    .then(() => {
        window.location.href = '/login';
    })
    .catch(error => {
        console.error('Logout failed:', error);
    });
}

// Prevent accidental page navigation when editing
window.addEventListener('beforeunload', function(e) {
    const editor = document.getElementById('editor');
    if (editor && editor.getAttribute('data-modified') === 'true') {
        e.preventDefault();
        e.returnValue = '';
    }
});

// Handle editor modifications
if (document.getElementById('editor')) {
    const editor = document.getElementById('editor');
    editor.addEventListener('input', function() {
        this.setAttribute('data-modified', 'true');
    });
} 