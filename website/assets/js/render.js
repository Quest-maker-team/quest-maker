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
    static RenderNewBlock(quest, question, instance, sourceEndpoint, targetEndpoint, blockType){
        let content = "<h5 class=\"card-title text-center\">"+blockType+"</h5>" +
                        "<hr>" +
                        "<p class=\"card-text text-center text-truncate\">"+ question.text +"</p>";
       
        let block = this.RenderBlock(question.question_id, "15rem", content);
        let answerTable = document.createElement("ul");
        answerTable.className = "list-group list-group-flush";  
        if(blockType!="Movement"){
            for (let answer of question.answer_options) {
                let tableElement = document.createElement("li");
                tableElement.innerHTML = answer.text;
                tableElement.className = "list-group-item";
                answerTable.append(tableElement);
                instance.addEndpoint(tableElement, {anchor: ["Right", "Left"]}, sourceEndpoint);
            }
            
        }else {
            for(let movement of question.movements){
                let tableElement = document.createElement("li");
                tableElement.innerHTML = movement.next_question_id;
                tableElement.className = "list-group-item";
                answerTable.append(tableElement);
                instance.addEndpoint(tableElement, {anchor: ["Right", "Left"]}, sourceEndpoint);
            }
        }
        block.append(answerTable);
        quest.AddDeleteButton(block, answerTable.childNodes, instance);

        instance.manage(block, block.id);
        instance.addEndpoint(block, targetEndpoint);

        return block;
    }

   
    static Render(quest,instance, sourceEndpoint, targetEndpoint) {
        this.RenderStart(quest.data.questions.find(question => question.type === "start"), instance, sourceEndpoint);
        this.RenderFinish(quest.data.questions.find(question => question.type === "end"), instance, targetEndpoint);
        this.RenderNewBlock(quest,quest.data.questions.find(question => question.type === "open"), instance, sourceEndpoint, targetEndpoint,"Open");
        this.RenderNewBlock(quest,quest.data.questions.find(question => question.question_id == 11), instance, sourceEndpoint, targetEndpoint,"Movement");
    }
}