import { cleanupQuestion } from "./models";

test("Cleanup question", ()=>{
    const a = [{
        question: "Burgos",
        answer: "burgos"
    },{
        question: "Soria",
        answer: "soria"
    }];
    const result = cleanupQuestion(a);
    expect(result).toBeInstanceOf(Array);
    expect(result[0]).toStrictEqual({
        question: "Burgos",
        answer: "burgos",
        done: false
    });
    expect(result[1]).toStrictEqual({
        question: "Soria",
        answer: "soria",
        done: false
    });
});