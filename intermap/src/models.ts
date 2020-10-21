export interface Question {
    question: string;
    answer: string;
    done: boolean;
}

export interface QuizState {
    score: number;
    questions: Question[];
    time: number;
    activeQuestion: Question | null;
}

export function cleanupQuestion(origin: any[]): Question[]{
    return origin.map((original)=>{
        return {
            question: original.question,
            answer: original.answer,
            done: false,
        }
    });
}

export interface Score{
    quiz: string;
    user: string;
    score: number;
    time: number;
}