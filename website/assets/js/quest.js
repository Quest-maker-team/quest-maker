export class Quest{
    constructor(data) {
        this.data = data;
    }

    DeleteQuestion(id, questions){
        questions.splice(questions.indexOf(questions.find(question => question.question_id == id)), 1);
    }

    AddDeleteButton(block, answerElements, instance){
        let deleteButton = document.createElement("button");
        deleteButton.id = "btn" + block.id;
        deleteButton.className = "btn-close btn-danger";
        deleteButton.style.position = "absolute";
        deleteButton.style.top = "0";
        deleteButton.style.right = "0";
        deleteButton.onclick = () => {
            for (let answerElement of answerElements) {
                instance.deleteConnectionsForElement(answerElement);
                instance.selectEndpoints({element: answerElement}).deleteAll();
            }
            instance.deleteConnectionsForElement(block);
            instance.selectEndpoints({element: block}).deleteAll();
            block.parentElement.removeChild(block);
            this.DeleteQuestion(block.id, this.data.questions);
        };
        block.append(deleteButton);
    }




   
}