export interface Question{
    id:number;
    text: string;
    type: "MCQ" | "SCQ" | "short_answer"; 
    options?: string[]; 
}