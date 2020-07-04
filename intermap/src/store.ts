import {QuizState, Question, cleanupQuestion} from "./models";

class Store implements QuizState {
    score = 0;
    questions: Question[] = [];
    time = 0;
    activeQuestion: Question | null = null;

    callback: (state: QuizState) => void;

    constructor(){
        this.callback = (state: QuizState) => {

        };
    }

    selectQuestion(): void{
        const answers = this.questions.filter((question)=> !question.done);
        if(answers.length > 0){
            const rnd = Math.floor(Math.random() * answers.length);
            this.activeQuestion = answers[rnd];
        }else{
            this.activeQuestion = null;
        }
    }

    setQuestions(newQuestions: Question[]): void{
        this.questions = newQuestions;
        this.selectQuestion();
        this.callback(this);
    }

    submitAnswer(answer: string): void{
        if(this.activeQuestion){
            if(answer === this.activeQuestion.answer){
                this.activeQuestion.done = true;
                this.selectQuestion();
                this.score += 25;
            }else{
                this.score = Math.max(0, this.score-10);
            }
            this.callback(this);
        }
    }

    tick(): void{
        if(this.activeQuestion){
            this.time += 1;
        }
        this.callback(this);
    }

    subscribe(callback: (state: QuizState) => void): void{
        this.callback = callback;
    }
}

const store = new Store();

export default store;