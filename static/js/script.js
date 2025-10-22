// JavaScript for AfiyaPal Blog

document.addEventListener('DOMContentLoaded', function() {
    // Category Filter Functionality
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            const category = this.getAttribute('data-category');
            filterPosts(category);
        });
    });
    
    const filterPosts = (category) => {
        const posts = document.querySelectorAll('.blog-post');
        
        posts.forEach(post => {
            if (category === 'all') {
                post.classList.remove('hidden');
            } else {
                const postCategory = post.getAttribute('data-category');
                if (postCategory === category) {
                    post.classList.remove('hidden');
                } else {
                    post.classList.add('hidden');
                }
            }
        });
    };

    // Comment Form Submission
    const commentForm = document.getElementById('commentForm');
    const commentsList = document.getElementById('commentsList');
    
    commentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const name = document.getElementById('name').value;
        const comment = document.getElementById('comment').value;
        
        if (name && comment) {
            addComment(name, comment);
            commentForm.reset();
        }
    });
    
    function addComment(name, text) {
        const commentDiv = document.createElement('div');
        commentDiv.className = 'comment';
        
        const currentDate = new Date().toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        commentDiv.innerHTML = `
            <div class="comment-header">
                <span class="comment-author">${name}</span>
                <span class="comment-date">${currentDate}</span>
            </div>
            <p class="comment-text">${text}</p>
        `;
        
        commentsList.prepend(commentDiv);
        
        // Show success message
        showNotification('Comment posted successfully!');
    }
    
    function showNotification(message) {
        const notification = document.createElement('div');
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background-color: #2c5aa0;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            transition: opacity 0.3s;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    // Add animation to blog posts when they come into view
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Apply initial styles for animation
    const blogPosts = document.querySelectorAll('.blog-post');
    blogPosts.forEach(post => {
        post.style.opacity = '0';
        post.style.transform = 'translateY(20px)';
        post.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(post);
    });

    console.log('AfiyaPal Blog loaded successfully!');
});