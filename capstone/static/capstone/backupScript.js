

// --- These codes are the same as the js codes found in input.html ---


document.addEventListener("DOMContentLoaded", function() {
    const addSiteButton = document.getElementById("add_sites");
    const siteFormContainer = document.getElementById("siteFormContainer");
    const cancelButton = document.getElementById("cancelButton");
    const contentText = document.getElementById("contentText");
    const iframeContainer = document.getElementById("iframe");
    let formVisible = false;
    const siteNameInput = document.getElementById("site_name");
    const siteURLInput = document.getElementById("site_url");

    const addNoteButton = document.getElementById("add_note");
    const noteFormContainer = document.getElementById("noteFormContainer");
    const cancelNoteButton = document.getElementById("cancelNoteButton");

    const notesContent = document.getElementById("notesContent");
    const notesContainer = document.getElementById("notesContainer");

    addNoteButton.addEventListener("click", function() {
        noteFormContainer.style.display = "block";
        siteFormContainer.style.display = "none";
        contentText.style.display = "none";
        iframeContainer.style.display = "none";
        notesContent.style.display = "none";
        formVisible = true;
    });

    cancelNoteButton.addEventListener("click", function() {
        siteFormContainer.style.display = "none";
        contentText.style.display = "block";
        iframeContainer.style.display = "block";
        formVisible = false;
        noteFormContainer.style.display = "none";
        notesContent.style.display = "none";
    });
    
    addSiteButton.addEventListener("click", function() {
        siteFormContainer.style.display = "block";
        contentText.style.display = "none";
        iframeContainer.style.display = "none";
        formVisible = true;
        noteFormContainer.style.display = "none";
        notesContent.style.display = "none";
    });

    cancelButton.addEventListener("click", function() {
        siteFormContainer.style.display = "none";
        contentText.style.display = "block";
        iframeContainer.style.display = "block";
        formVisible = false;
        noteFormContainer.style.display = "none";
        notesContent.style.display = "none";
    });

    const addSiteForm = document.getElementById("siteForm");

    addSiteForm.addEventListener("submit", function(event) {
        const siteNameInput = document.getElementById("site_name");
        const siteURLInput = document.getElementById("site_url");

        const siteName = siteNameInput.value;
        const siteURL = siteURLInput.value;

        const extractedSiteName = getSiteNameFromURL(siteURL);

        if (extractedSiteName) {
            siteNameInput.value = extractedSiteName;

            if (siteURL.includes("devdocs") || extractedSiteName.includes("devdocs")) {

            const iframe = document.createElement("iframe");
            iframe.src = siteURL;
            iframe.style.width = "100%";
            iframe.style.height = "500px";
            iframeContainer.innerHTML = '';
            iframeContainer.appendChild(iframe);
        } else {
            const newLink = document.createElement("a");
            newLink.href = siteURL; 
            newLink.target = "_blank"; 
            newLink.rel = "noopener noreferrer"; 
            newLink.innerText = extractedSiteName;           
            const linksContainer = document.querySelector("#linksContainer");
            linksContainer.appendChild(newLink);
        }

        siteFormContainer.style.display = "none";
        contentText.style.display = "block";
        formVisible = false;
    } else {
        alert("Error !!!");
    }
});

function getSiteNameFromURL(url) {
const domainStart = url.indexOf("://") > -1 ? url.indexOf("://") + 3 : 0; 
const pathStart = url.indexOf("/", domainStart); 


const domainEnd = pathStart > -1 ? pathStart : url.length;


const domain = url.substring(domainStart, domainEnd);

const parts = domain.split(".");
const extensions = [".com", ".net", ".org", ".xyz", ".io"];

for (let i = 0; i < parts.length; i++) {
    const part = parts[i];
    if (i === 0) {

        if (part.startsWith("www")) {
            parts[i] = parts[i].substring(4);
        } else if (extensions.includes("." + part)) {
            parts.splice(i, 1);
            i--;
        }
    } else if (extensions.includes("." + part)) {

        parts.splice(i, 1);
        i--;
    }
}


const siteName = parts.join("");

return siteName || null;
}



    fetch("{% url 'get_sites' input.id %}")
        .then(response => response.json())
        .then(data => {
            const linksContainer = document.getElementById("linksContainer");
            linksContainer.innerHTML = "";
            data.sites.forEach(site => {
            if (site.name.includes("devdocs") || site.url.includes("devdocs")) {
                const iframe = document.createElement("iframe");
                iframe.src = site.url;
                iframe.style.width = "100%";
                iframe.style.height = "500px";
                iframeContainer.innerHTML = '';
                iframeContainer.appendChild(iframe);

                const devdocsLink = document.createElement("a");
                devdocsLink.innerText = "devdocs";
                devdocsLink.href = "#";
                devdocsLink.className = "link list-group-item ms-1 px-1 py-1";
                devdocsLink.style.backgroundColor = "#F2F2F2"
                linksContainer.appendChild(devdocsLink);
            } else {
                const newLink = document.createElement("a");
                newLink.target = "_blank";
                newLink.rel = "noopener noreferrer";
                newLink.href = site.url.startsWith('http') ? site.url : 'http://' + site.url;
                newLink.className = "link list-group-item ms-1 px-1 py-1";
                newLink.innerHTML = site.name + ' <i class="fas fa-external-link-alt fa-xxs" title="Will open in a new tab"></i>';
                newLink.style.backgroundColor = "#F2F2F2"
                linksContainer.appendChild(newLink);
            }
    });
});


fetch("{% url 'get_notes' input.id %}")
.then(response => response.json())
.then(data => {
    const notesContainer = document.getElementById("notesContainer");
    notesContainer.innerHTML = "";
    data.notes.forEach(note => {
        const noteElement = document.createElement("a");
        noteElement.className = "link list-group-item ms-1 px-1 py-2";
        noteElement.innerHTML = `${note.title} <i class="fas fa-chevron-circle-right fa-xxs"></i>`;
        noteElement.style.backgroundColor = "#F2F2F2"
        noteElement.href = "#"
        notesContainer.appendChild(noteElement);
    });
});


fetch(`{% url 'get_notes' input.id %}`)
.then(response => response.json())
.then(data => {
    const notesData = data;
    const notesContainer = document.getElementById("notesContainer");

    let noteElement;

    document.getElementById("notesContainer").addEventListener("click", function(event) {
        notesContent.style.display = "block";
        contentText.style.display = "none";
        iframeContainer.style.display = "none";
        formVisible = true;
        noteFormContainer.style.display = "none";
        siteFormContainer.style.display = "none";
        if (event.target.tagName === "A") {
            event.preventDefault(); 
            const noteTitle = event.target.textContent.trim();
            const notesContent = document.getElementById("notesContent");
            const notesContentContent = document.getElementById("notesContentContent");
            const notesContentTitle = document.getElementById("notesContentTitle");
            const notesContentOwner = document.getElementById("notesContentOwner");
            const notesContentButtons = document.getElementById("noteButtons");

            const selectedNote = notesData.notes.find(note => note.title === noteTitle);

            if (selectedNote) {

                if (notesContentTitle) {
                    notesContentTitle.innerHTML = `${selectedNote.title}`;
                }
                if (notesContentContent) {
                    notesContentContent.innerHTML = `${selectedNote.content}`;
                }
                if (notesContentOwner) {


                    const datePosted = new Date(selectedNote.date_posted);
                    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', timeZoneName: 'short' };
                    const formattedDate = datePosted.toLocaleDateString('en-US', options);

                    notesContentOwner.innerHTML = `Posted by <strong style="color: red;">${selectedNote.owner}</strong> on ${formattedDate}`;
                }
                if (notesContentButtons) {
                    notesContentButtons.innerHTML = `
                    <button id="note_edit" type="button" class="btn btn-sm btn-warning" data-note-id="{{ note.id }}" style="color: white;"><i class="far fa-edit"></i> Edit ${selectedNote.id}</button>
                    
                    <button id="note_delete" type="button" class="btn btn-sm btn-danger" data-note-id="{{ note.id }}"><i class="far fa-trash-alt"></i> Delete ${selectedNote.id}</button>
                    
                    <button id="note_save" type="button" class="btn btn-sm btn-success" data-note-id="{{ note.id }}"><i class="far fa-save"></i> Save ${selectedNote.id}</button>
                    
                    <button id="note_cancel" type="button" class="btn btn-sm btn-secondary" data-note-id="{{ note.id }}"><i class="far fa-xmark"></i> Cancel ${selectedNote.id}</button>`
                }

                const noteOwner = `${selectedNote.owner}`;
                const authenticatedUser = "{{ user.username }}";
                const editButton = document.getElementById("note_edit");
                const deleteButton = document.getElementById("note_delete");
                const saveButton = document.getElementById("note_save");
                const cancelButton = document.getElementById("note_cancel");

        
                if (noteOwner != authenticatedUser) {
                editButton.style.display = "none";
                deleteButton.style.display = "none";
                saveButton.style.display = "none";
                cancelButton.style.display = "none";
                }

                noteElement = event.target;

                const editButtons = document.getElementById("note_edit");
                editButtons.addEventListener("click", function() {
                    toggleEditability(true);
                });

                function toggleEditability(editMode) {
                    if (editMode) {
                        notesContentTitle.contentEditable = "true";
                        notesContentContent.contentEditable = "true";
                        notesContentTitle.style.border = "2px solid #ccc";
                        notesContentContent.style.border = "2px solid #ccc";
                        notesContentTitle.style.backgroundColor = "#fff";
                        notesContentContent.style.backgroundColor = "#fff";
                    } else {
                        notesContentTitle.contentEditable = "false";
                        notesContentContent.contentEditable = "false";
                        notesContentTitle.style.border = "none";
                        notesContentContent.style.border = "none";
                        notesContentTitle.style.backgroundColor = "transparent";
                        notesContentContent.style.backgroundColor = "transparent";
                    }
                }
               
                const cancelNoteButton = document.getElementById("note_cancel");

                cancelNoteButton.addEventListener("click", function () {
                    toggleEditability(false);
                });

                function toggleEditability(editMode) {
                    if (editMode) {
                        notesContentTitle.contentEditable = "true";
                        notesContentContent.contentEditable = "true";
                        notesContentTitle.style.border = "2px solid #ccc";
                        notesContentContent.style.border = "2px solid #ccc";
                        notesContentTitle.style.backgroundColor = "#fff";
                        notesContentContent.style.backgroundColor = "#fff";
                    } else {
                        notesContentTitle.contentEditable = "false";
                        notesContentContent.contentEditable = "false";
                        notesContentTitle.style.border = "none";
                        notesContentContent.style.border = "none";
                        notesContentTitle.style.backgroundColor = "transparent";
                        notesContentContent.style.backgroundColor = "transparent";
                    }
                }

                const saveButtons = document.getElementById("note_save");
                    
                var csrftoken = "{{ csrf_token }}";

                saveButtons.addEventListener("click", function() {
                    const noteId = selectedNote.id;
                    const newTitle = notesContentTitle.textContent;
                    const newContent = notesContentContent.textContent;
                    toggleEditability(false);

                    fetch(`/edit_note/${noteId}/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'X-CSRFToken': csrftoken
                        },
                        body: `title=${encodeURIComponent(newTitle)}&content=${encodeURIComponent(newContent)}`
                        
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            console.error(data.error);
                            console.log("ERROR !!!!!");
                        } else {
                            console.log(data.message);
                            console.log("EDIT Successful !!!");
                            window.location.reload();
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                })

                const deleteNoteButton = document.getElementById("note_delete");

                deleteNoteButton.addEventListener("click", function () {
                const noteId = selectedNote.id;
                const noteOwner = selectedNote.owner;
                const confirmed = confirm(`Are you sure you want to delete the note?`);
                    if (confirmed) {
                fetch(`/delete_note/${noteId}/`, {
                method: 'DELETE',
                headers: {
                'X-CSRFToken': csrftoken,
                },
            })
            .then(response => {
                if (response.ok) {
                    const deletemsg = document.getElementsByClassName("alertMsg")[0];
                    deletemsg.style.display = "block";
                    notesContent.style.display ="none";
                    contentText.style.display = "block";
                    iframeContainer.style.display = "block";
                    
                    notesContainer.removeChild(noteElement);
                } else if (response.status === 403) {
                    const deletemsg = document.getElementsByClassName("alertMsg")[0];
                    deletemsg.style.display = "block";
                    const alertmsg = document.getElementById("alertMsg");
                    alertmsg.innerHTML = "You are not the owner of this note, so you cannot delete it."

                } else {
                    alert('Error!!! Note deletion failed.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
            } else {
                console.log('Transaction canceled.');
            }
        });
            }
        }
    });
});

linksContainer.addEventListener("click", function(event) {
if (event.target.tagName === "A") {
    const clickedLink = event.target;

    if (clickedLink.textContent.includes("devdocs")) {
        siteFormContainer.style.display = "none";
        contentText.style.display = "block";
        iframeContainer.style.display = "block";
        formVisible = false;
        noteFormContainer.style.display = "none";
        notesContent.style.display = "none";
    }
}
});

const editCommentElements = document.querySelectorAll(".edit-comment-button");

editCommentElements.forEach((editCommentElement) => {
editCommentElement.addEventListener("click", () => {
    const commentId = editCommentElement.getAttribute("data-comment-id");
    const commentElement = document.getElementById(`comment-${commentId}`);
    
    commentElement.setAttribute("contenteditable", "true");
    commentElement.focus();
    
    editCommentElement.style.display = "none";
    
    const saveButton = document.createElement("button");
    saveButton.className = "btn btn-sm btn-success save-comment-button";
    const saveIcon = document.createElement("i");
    saveIcon.className = "far fa-save";
    const saveText = document.createTextNode(" Save");
    saveButton.appendChild(saveIcon);
    saveButton.appendChild(saveText);
    commentElement.parentElement.appendChild(saveButton);
    
    
    saveButton.addEventListener("click", () => {
        commentElement.setAttribute("contenteditable", "false");
        
        const editedMessage = commentElement.textContent;
        
        saveEditedComment(commentId, editedMessage);
        
        saveButton.style.display = "none";
        editCommentElement.style.display = "inline-block";
    });
});
});

function saveEditedComment(commentId, editedMessage) {
const csrftoken = "{{ csrf_token }}";

fetch(`/edit_comment/${commentId}/`, {
    method: "POST",
    headers: {
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `message=${encodeURIComponent(editedMessage)}`,
})
    .then((response) => response.json())
    .then((data) => {
        if (data.message) {
            const successCommentClass = document.getElementsByClassName("successComment")[0];
            successCommentClass.style.display = "block";
            const successComment = document.getElementById("successComment");
            successComment.innerHTML = "<strong>SUCCESS !!!</strong> Your comment has been saved successfully."

            const deleteCommentClass = document.getElementsByClassName("deleteComment")[0];
            deleteCommentClass.style.display = "none";
        } else if (data.error) {
            console.error("Error:", data.error);
        }
    });
}

const deleteCommentElements = document.querySelectorAll(".delete-comment-button");

deleteCommentElements.forEach((deleteCommentElement) => {
    deleteCommentElement.addEventListener("click", (event) => {
        event.preventDefault();
        
        const commentId = deleteCommentElement.getAttribute("data-comment-id");
        
        const isConfirmed = confirm("Bu yorumu silmek istediğinizden emin misiniz?");
        
        if (isConfirmed) {
            deleteComment(commentId);
        }
    });
});

function deleteComment(commentId) {
    const csrftoken = "{{ csrf_token }}";

    fetch(`/delete_comment/${commentId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/x-www-form-urlencoded",
        },
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.message) {
            const commentElement = document.getElementById(`comment-${commentId}`);
            if (commentElement) {
                commentElement.parentElement.parentElement.remove();
                const deleteCommentClass = document.getElementsByClassName("deleteComment")[0];
                deleteCommentClass.style.display = "block";
                const deleteComment = document.getElementById("deleteComment");
                deleteComment.innerHTML = "<strong>DELETED !!!</strong> Your comment has been deleted successfully."

                const successCommentClass = document.getElementsByClassName("successComment")[0];
                successCommentClass.style.display = "none";
            }
        } else if (data.error) {
            console.error("Hata:", data.error);
        }
    });
}
});

document.querySelectorAll('.emoji-option').forEach(function(emojiOption) {
emojiOption.addEventListener('click', function() {
    const emoji = emojiOption.textContent;
    const newCommentInput = document.getElementById('newComment');
    newCommentInput.value += emoji;
});
});


const emojiOptions = document.querySelectorAll('.emoji-option');

emojiOptions.forEach(emoji => {
emoji.addEventListener('click', () => {
    emoji.style.transform = 'scale(0.9)';
    
    setTimeout(() => {
        emoji.style.transform = 'scale(1)';
    }, 100);
});
});

document.getElementById('noteForm').addEventListener('submit', function (e) {
        const noteTitleInput = document.getElementById('note_title');

        const noteTitleValue = noteTitleInput.value.trim();

        if (noteTitleValue.length > 17) {
            e.preventDefault();
            alert('Title must be 17 characters or less.');
        }
    });


    document.addEventListener("DOMContentLoaded", function() {
        const scrollTopButton = document.getElementById("scrollTopButton");
        
        scrollTopButton.addEventListener("click", function() {
            event.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
        
        const scrollBottomButton = document.getElementById("scrollBottomButton");
        
        
        scrollBottomButton.addEventListener("click", () => {
            event.preventDefault();
            window.scrollTo({
            top: document.body.scrollHeight,
            behavior: "smooth"
          });
        });
        });

        document.getElementById('myForm').addEventListener('submit', function (e) {
            const titleInput = document.getElementById('title');
    
            const titleValue = titleInput.value.trim();
    
            if (titleValue.length > 30) {
                e.preventDefault();
                alert('Title must be 30 characters or less.');
            }
        });