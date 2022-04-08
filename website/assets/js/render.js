export class Render{
    static RenderBlock(id, width, cardBody){
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

    static RenderStart(question, instance, sourceEndpoint){
        let content = "<h5 class=\"card-title text-center\">Start</h5>" +
                        "<hr>" +
                        "<p class=\"card-text text-center text-truncate\">"+ question.text +"</p>";
        let block = this.RenderBlock(question.question_id, "10rem", content);
        instance.manage(block, block.id);
        instance.addEndpoint(block, sourceEndpoint);
    }

    static RenderFinish(question, instance, targetEndpoint){
        let content = "<h5 class=\"card-title text-center\">Finish</h5>" +
                        "<hr>" +
                        "<p class=\"card-text text-center text-truncate\">"+ question.text +"</p>";
        let block = this.RenderBlock(question.question_id, "10rem", content);
        instance.manage(block, block.id);
        instance.addEndpoint(block, targetEndpoint);
    }

    static renderOpenQuestion(quest, question, instance, sourceEndpoint, targetEndpoint){
        let content = "<h5 class=\"card-title text-center\">Open</h5>" +
                        "<hr>" +
                        "<p class=\"card-text text-center text-truncate\">" + question.text + "</p>";
        let block = Render.RenderBlock(question.question_id, "15rem", content);
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
        quest.AddDeleteButton(block, instance, answerTable.childNodes);

        instance.addEndpoint(block, {anchor: "Top"}, targetEndpoint);

        return block;
    }

    static  renderMovement(quest, question, instance, sourceEndpoint, targetEndpoint){
        let content = "<h5 class=\"card-title text-center\">Movement</h5>" +
                        "<hr>" +
                        "<p class=\"card-text text-center text-truncate\">" + question.text + "</p>";
        let block = Render.RenderBlock(question.question_id, "15rem", content);
        quest.AddDeleteButton(block, instance);

        instance.addEndpoint(block, {anchor: "Top"}, targetEndpoint);
        instance.addEndpoint(block, {anchor: "Bottom"}, sourceEndpoint);

        return block;
    }
   
    static Render(quest, instance, sourceEndpoint, targetEndpoint) {
        Render.RenderStart(quest.data.questions.find(question => question.type === "start"), instance, sourceEndpoint);
        Render.RenderFinish(quest.data.questions.find(question => question.type === "end"), instance, targetEndpoint);
        Render.renderOpenQuestion(quest, quest.data.questions.find(question => question.type === "open"), instance, sourceEndpoint, targetEndpoint);
        Render.renderMovement(quest, quest.data.questions.find(question => question.question_id == 11), instance, sourceEndpoint, targetEndpoint);
    }
}