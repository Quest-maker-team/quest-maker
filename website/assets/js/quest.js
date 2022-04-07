export class Quest{
    constructor(data) {
        this.data = data;
    }

    RenderBlock(id, width, cardBody){
        let block = document.createElement("div");
        block.id = id;
        block.className = "position-absolute border-2 card";

        let blockBody = document.createElement("div");
        blockBody.className = "card-body";
        blockBody.innerHTML = cardBody;
        block.style.width = width;
        block.append(blockBody);

        document.getElementById("container").append(block);
        return block;
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

    RenderStart(question, instance, sourceEndpoint){
        let content = "<h5 class=\"card-title text-center\">Start</h5>" +
                        "<hr>" +
                        "<p class=\"card-text text-center text-truncate\">"+ question.text +"</p>";
        let block = this.RenderBlock(question.question_id, "10rem", content);
        instance.manage(block, block.id);
        instance.addEndpoint(block, sourceEndpoint);
    }

    RenderFinish(question, instance, targetEndpoint){
        let content = "<h5 class=\"card-title text-center\">Finish</h5>" +
                        "<hr>" +
                        "<p class=\"card-text text-center text-truncate\">"+ question.text +"</p>";
        let block = this.RenderBlock(question.question_id, "10rem", content);
        instance.manage(block, block.id);
        instance.addEndpoint(block, targetEndpoint);
    }

    RenderOpenQuestion(question, instance, sourceEndpoint, targetEndpoint){
        let content = "<h5 class=\"card-title text-center\">Open</h5>" +
                        "<hr>" +
                        "<p class=\"card-text text-center text-truncate\">"+ question.text +"</p>";
        console.log(question.answer_options);
        let block = this.RenderBlock(question.question_id, "15rem", content);

        let answerTable = document.createElement("ul");
        answerTable.className = "list-group list-group-flush";
        for (let answer of question.answer_options) {
            let tableElement = document.createElement("li");
            tableElement.innerHTML = answer.text;
            tableElement.className = "list-group-item";
            answerTable.append(tableElement);
            instance.addEndpoint(tableElement, {anchor: ["Right", "Left"]}, sourceEndpoint);
        }
        block.append(answerTable);

        this.AddDeleteButton(block, answerTable.childNodes, instance);

        instance.manage(block, block.id);
        instance.addEndpoint(block, targetEndpoint);

        return block;
    }

    Render(instance, sourceEndpoint, targetEndpoint) {
        this.RenderStart(this.data.questions.find(question => question.type === "start"), instance, sourceEndpoint);
        this.RenderFinish(this.data.questions.find(question => question.type === "end"), instance, targetEndpoint);
        //console.log(quest.questions.find(question => question.type === "open"));
        this.RenderOpenQuestion(this.data.questions.find(question => question.type === "open"), instance, sourceEndpoint, targetEndpoint);
        this.RenderOpenQuestion(this.data.questions.find(question => question.question_id == 8), instance, sourceEndpoint, targetEndpoint);
    }
}