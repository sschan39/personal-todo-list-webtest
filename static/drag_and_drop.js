const todoList = document.getElementById('todo-list');
let draggedItem = null;

todoList.addEventListener('dragstart', (e) => {
    if (e.target && e.target.classList.contains('draggable')) {
        draggedItem = e.target;
        e.target.style.opacity = '0.5';
        e.dataTransfer.effectAllowed = 'move';
    }
});

todoList.addEventListener('dragend', (e) => {
    if (e.target && e.target.classList.contains('draggable')) {
        e.target.style.opacity = '1';
        draggedItem = null;
    }
});

todoList.addEventListener('dragover', (e) => {
    e.preventDefault();
    const target = e.target.closest('.draggable');
    if (target && target !== draggedItem) {
        target.classList.add('drag-over');
    }
});

todoList.addEventListener('dragleave', (e) => {
    const target = e.target.closest('.draggable');
    if (target) {
        target.classList.remove('drag-over');
    }
});

todoList.addEventListener('drop', (e) => {
    e.preventDefault();
    const target = e.target.closest('.draggable');
    if (target && target !== draggedItem) {
        target.classList.remove('drag-over');

        // Determine the position to insert the dragged item
        const bounding = target.getBoundingClientRect();
        const offset = e.clientY - bounding.top;

        if (offset > bounding.height / 2) {
            // Insert after the target
            todoList.insertBefore(draggedItem, target.nextSibling);
        } else {
            // Insert before the target
            todoList.insertBefore(draggedItem, target);
        }

        // Update the priority numbers in the DOM
        updatePriorityNumbers();

        // Immediately send the new order to the server
        const newOrder = Array.from(todoList.children).map((item) => item.dataset.id);
        fetch('/update-priority', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ order: newOrder }),
        })
            .then((response) => {
                if (response.ok) {
                    console.log('Priority updated successfully');
                } else {
                    console.error('Failed to update priority');
                }
            })
            .catch((error) => console.error('Error:', error));
    }
});

// Function to update priority numbers in the DOM
function updatePriorityNumbers() {
    const items = Array.from(todoList.children);
    items.forEach((item, index) => {
        const priorityElement = item.querySelector('strong');
        if (priorityElement) {
            priorityElement.textContent = `${index + 1}.`;
        }
    });
}