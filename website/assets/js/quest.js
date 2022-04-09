export class Quest{
    constructor(data) {
        this.data = data;
    }

    deleteQuestion(id){
        let questions = this.data.questions;
        questions.splice(questions.indexOf(questions.find(question => question.question_id == id)), 1);
    }

    updateQuestionText(id, text){
        let questions = this.data.questions;
        questions.find(question => question.question_id == id).text = text;
    }
}