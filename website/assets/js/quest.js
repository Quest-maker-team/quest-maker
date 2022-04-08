export class Quest{
    constructor(data) {
        this.data = data;
    }

    DeleteQuestion(id, questions){
        questions.splice(questions.indexOf(questions.find(question => question.question_id == id)), 1);
    }

    AddDeleteButton(block, instance, answerElements){
        let deleteButton = document.createElement("button");
        deleteButton.id = "btn" + block.id;
        deleteButton.className = "btn-close btn-danger";
        deleteButton.style.position = "absolute";
        deleteButton.style.top = "0";
        deleteButton.style.right = "0";
        deleteButton.onclick = () => {
            console.log(answerElements !== undefined);
            if (answerElements !== undefined)
            for (let answerElement of answerElements) {
                console.log(answerElement);
                instance.deleteConnectionsForElement(answerElement);
                instance.selectEndpoints({element: answerElement}).deleteAll();
                delete instance.getManagedElements()[answerElement.id];
            }
            instance.deleteConnectionsForElement(block);

            instance.selectEndpoints({element: block}).deleteAll();
            delete instance.getManagedElements()[block.id];
            block.parentElement.removeChild(block);
            this.DeleteQuestion(block.id, this.data.questions);
        };
        block.append(deleteButton);
    }
}