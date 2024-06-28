
function getCaretPosition(element) {
    let caretOffset = 0;
    const doc = element.ownerDocument || element.document;
    const win = doc.defaultView || doc.parentWindow;
    const sel = win.getSelection();
    if (sel.rangeCount > 0) {
        const range = sel.getRangeAt(0);
        const preCaretRange = range.cloneRange();
        preCaretRange.selectNodeContents(element);
        preCaretRange.setEnd(range.endContainer, range.endOffset);
        caretOffset = preCaretRange.toString().length;
    }
    return caretOffset;
}

function setCaretPosition(element, offset) {
    const doc = element.ownerDocument || element.document;
    const win = doc.defaultView || doc.parentWindow;
    const range = doc.createRange();
    const sel = win.getSelection();
    range.setStart(element, 0);
    range.collapse(true);
    sel.removeAllRanges();
    sel.addRange(range);

    let charIndex = 0;
    const nodeStack = [element];
    let node;
    let foundStart = false;

    while ((node = nodeStack.pop()) && !foundStart) {
        if (node.nodeType === 3) { // Text node
            const nextCharIndex = charIndex + node.length;
            if (!foundStart && offset >= charIndex && offset <= nextCharIndex) {
                range.setStart(node, offset - charIndex);
                foundStart = true;
            }
            charIndex = nextCharIndex;
        } else {
            let i = node.childNodes.length;
            while (i--) {
                nodeStack.push(node.childNodes[i]);
            }
        }
    }
    sel.removeAllRanges();
    sel.addRange(range);
}


function handleTabKey(event) {
    const codeBlock = document.getElementById('editableCode');
    const TAB_SIZE = 4;
    if (event.key === 'Tab') {
        event.preventDefault();

        const caretPosition = getCaretPosition(codeBlock);
        const currentText = codeBlock.textContent;

        // Insert tab character (or spaces) at the caret position
        const newText = currentText.slice(0, caretPosition) + ' '.repeat(TAB_SIZE) + currentText.slice(caretPosition);

        codeBlock.textContent = newText;

        // Restore the caret position after inserting the tab
        setCaretPosition(codeBlock, caretPosition + TAB_SIZE);

        // Re-highlight the code block
        syncAndHighlight();
    }
}



// Function to synchronize the content from textarea to the <pre><code> block and highlight it
function syncAndHighlight() {
    const codeBlock = document.getElementById('editableCode');
    const caretPosition = getCaretPosition(codeBlock);

    // Escape HTML to prevent injection attacks
    codeBlock.textContent = codeBlock.textContent.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');


    delete codeBlock.dataset.highlighted
    // Highlight the content of the code block
    hljs.highlightElement(codeBlock);
    // Restore the cursor position
    setCaretPosition(codeBlock, caretPosition);
}

// Attach the handleTabKey function to the keydown event
editableCode.addEventListener('keydown', handleTabKey);

// Attach the updateHighlighting function to the input event of the <pre><code> block
document.getElementById('editableCode').addEventListener('input', syncAndHighlight);

// Initial call to updateHighlighting to ensure the initial content is highlighted
syncAndHighlight();