import {BlockRedactor} from "./blockRedactor";

export class Render{
    static renderBlockBase(question, width, title){
        let block = document.createElement("div");
        block.id = question.question_id;
        block.className = "position-absolute border-2 card";

        let blockBody = document.createElement("div");
        blockBody.className = "card-body";
        blockBody.innerHTML = "<h5 class=\"card-title text-center\">" + title + "</h5>" +
                                "<hr>" +
                                "<p class=\"card-text text-center text-truncate\">" + question.text + "</p>";
        block.style.width = width;
        block.append(blockBody);

        block.ondblclick = () => {
            BlockRedactor.showRedactor(question);
        }

        document.getElementById("container").append(block);
        return block;
    }

    static addDeleteButton(quest, block, instance, answerElements){
        let deleteButton = document.createElement("button");
        deleteButton.id = "btn" + block.id;
        deleteButton.className = "btn-close btn-danger";
        deleteButton.style.position = "absolute";
        deleteButton.style.top = "0";
        deleteButton.style.right = "0";
        deleteButton.onclick = () => {
            if (answerElements !== undefined) {
                for (let answerElement of answerElements) {
                    instance.deleteConnectionsForElement(answerElement);
                    instance.selectEndpoints({element: answerElement}).deleteAll();
                    delete instance.getManagedElements()[answerElement.id];
                }
            }
            instance.deleteConnectionsForElement(block);

            instance.selectEndpoints({element: block}).deleteAll();
            delete instance.getManagedElements()[block.id];
            block.parentElement.removeChild(block);
            let questions = quest.data.questions;
            questions.splice(questions.indexOf(questions.find(question => question.question_id == block.id)), 1);
        };
        block.append(deleteButton);
    }

    static renderStart(question, instance, sourceEndpoint){
        let block = this.renderBlockBase(question, "10rem", "Начало");
        instance.manage(block, block.id);
        instance.addEndpoint(block, sourceEndpoint);
    }

    static renderFinish(question, instance, targetEndpoint){
        let block = this.renderBlockBase(question, "10rem", "Конец");
        instance.manage(block, block.id);
        instance.addEndpoint(block, targetEndpoint);
    }

    static renderOpenQuestion(quest, question, instance, sourceEndpoint, targetEndpoint){
        let block = Render.renderBlockBase(question, "15rem", "Открытый вопрос");
        let answerTable = document.createElement("ul");
        answerTable.className = "list-group list-group-flush";
        block.append(answerTable);
        for (let answer of question.answer_options) {
            let tableElement = document.createElement("li");
            tableElement.innerHTML = answer.text;
            tableElement.className = "list-group-item";
            tableElement.id = "answer" + answer.answer_option_id;
            answerTable.append(tableElement);
            instance.addEndpoint(tableElement, {anchor: ["Right", "Left"]}, sourceEndpoint);
        }

        Render.addDeleteButton(quest, block, instance, answerTable.childNodes);

        instance.addEndpoint(block, {anchor: "Top"}, targetEndpoint);

        return block;
    }

    static  renderMovement(quest, question, instance, sourceEndpoint, targetEndpoint){
        let block = Render.renderBlockBase(question, "15rem", "Перемещение");

        Render.addDeleteButton(quest, block, instance);

        instance.addEndpoint(block, {anchor: "Top"}, targetEndpoint);
        instance.addEndpoint(block, {anchor: "Bottom"}, sourceEndpoint);

        return block;
    }

    static render(quest, instance, sourceEndpoint, targetEndpoint) {
        Render.renderStart(quest.data.questions.find(question => question.type === "start"), instance, sourceEndpoint);
        Render.renderFinish(quest.data.questions.find(question => question.type === "end"), instance, targetEndpoint);
        Render.renderOpenQuestion(quest, quest.data.questions.find(question => question.type === "open"), instance, sourceEndpoint, targetEndpoint);
        Render.renderMovement(quest, quest.data.questions.find(question => question.type === "movement"), instance, sourceEndpoint, targetEndpoint);
    }
}
