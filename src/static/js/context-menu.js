function showContextMenu(event, fileId) {
    event.preventDefault();

    const menu = document.getElementById('context-menu');
    const x = event.pageX;
    const y = event.pageY;
    const menuWidth = menu.offsetWidth;
    const menuHeight = menu.offsetHeight;

    const spaceRight = window.innerWidth - x;
    const spaceBottom = window.innerHeight - y;

    const leftPosition = (spaceRight < menuWidth) ? (x - menuWidth) : x;

    const topPosition = (spaceBottom < menuHeight) ? (y - menuHeight) : y;

    menu.style.left = `${Math.min(leftPosition, window.innerWidth - menuWidth)}px`;
    menu.style.top = `${Math.min(topPosition, window.innerHeight - menuHeight)}px`;


    menu.style.display = 'block';

    menu.setAttribute('dataId', fileId);
}

function hideContextMenu() {
    document.getElementById('context-menu').style.display = 'none';
}

function performAction(action) {
    const menu = document.getElementById('context-menu');
    const fileId = menu.getAttribute('dataId');
    let url = '';
    
    switch (action) {
        case 'download':
            url = `/download/${fileId}`;
            const tooltip = document.getElementById(`tooltip-${fileId}`);
            if (tooltip !== null){
                const parts = tooltip.textContent.trim().split(' ');
                const lastPart = parts[parts.length - 1];
                const downloads = parseInt(lastPart, 10);
                tooltip.textContent = `Downloads: ${downloads+1}`;
            }
            break;
        case 'delete':
            url = `/delete/${fileId}`;
            break;
        case 'toggleprivacy':
            url = `/toggleprivacy/${fileId}`;
            break;
        case 'toggleadmin':
            url = `users/toggleadmin/${fileId}`;
            break;
    }

    if (url) {
        window.location.href = url;
    }

    hideContextMenu();
}

document.addEventListener('click', function(event) {
    if (!event.target.closest('.context-menu') && !event.target.closest('.grid-item')) {
        hideContextMenu();
    }
});