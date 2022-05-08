function deleteQuestRequest(questId) {
    return new Promise(function(resolve, reject) {
        const xmlhttp = new XMLHttpRequest();
        xmlhttp.open('DELETE', 'api/personal_catalog/quest/' + questId);
        xmlhttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

        xmlhttp.onreadystatechange = () => {
            if (xmlhttp.readyState === XMLHttpRequest.DONE) {
                if (xmlhttp.status === 200) {
                    resolve(xmlhttp.response);
                } else {
                    reject(xmlhttp.status);
                }
            }
        };

        xmlhttp.send();
    });
}

function setActions() {
    const buttons = document.getElementsByName('deleteButton');
    for (const button of buttons) {
        button.onclick = () => {
            if (confirm('Вы уверены, что хотите удалить квест? Отменить это действие будет невозможно.')) {
                deleteQuestRequest(button.id);
                const ell = button.parentElement;
                ell.parentElement.removeChild(ell);
            }
        };
    }
}

setActions();
