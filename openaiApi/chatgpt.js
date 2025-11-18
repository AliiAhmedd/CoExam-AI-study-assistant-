// This file represents the code for the OpenAI subsystem. This subsystem is responsible for two things: to forward the request to chatGPT and return the response
import fs from "fs"
import OpenAI from "openai";

const openai = new OpenAI({apiKey:"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"});

const generateExam = async (filePath) => {
  const vectorID = await uploadFile(filePath) // Upload & retrieve id for file
  const assistantID = await createAssistant(vectorID) // Create new assistant (gpt instance with instructions), using given vectorID (uploaded PDF)
  const threadID = await createThread() // Create a new thread: a "conversation" for all messages in the current session

  const examQuestions = await runAssistant(threadID, assistantID) // Perform the prompt with the previously created thread & assistant
  return examQuestions
}

const uploadFile = async (filePath) => {

  // Upload the raw file to openai
  const fileData = await openai.files.create({
    file: fs.createReadStream(filePath),
    purpose: "assistants",
  });

  // Create space for the file (on openais server) for the raw pdf to be stored as embeddings ("chunks", numerical representation of the PDF)
  const vectorStore = await openai.vectorStores.create({
    name: "Module Curriculum VectorStore",
  });

  // Partitions the raw pdf (stored on openai's servers) into numeric vectors (embeddings), to be stored in the vector space made above ^
  await openai.vectorStores.files.createAndPoll(vectorStore.id, {
    file_id: fileData.id
  })

  return vectorStore.id // Return reference for assistant
};

const createAssistant = async (vectorID) => {
  const assistant = await openai.beta.assistants.create({
    name: "CoExam Practice-Paper Generator",
    instructions: "Your task is to generate a set of numbered practice questions based entriely on the content provided in the curriculum PDF. The questions should be a mix of multiple-choice, short written answers, and longer-form written questions. Do not answer with any confirmation of my prompt, only generate the paper. All the questions should total 100 marks; harder/ longer questions weighed higher. It is extremely important the questions you write are based entirely off the content provided in the PDF file. Do not cite any references from the PDF. IMPORTANT: Always give the answers AT THE END OF THE PAPER. Provide your output in Markdown formatting.",
    model: "gpt-4o",
    tools: [{ type: "file_search" }], // Enables PDF searching for this assistant
    tool_resources: { file_search: { vector_store_ids: [vectorID] } }, // Assistant searches the given vectorID (file upload)
  });

  return assistant.id;
};

const createThread = async () => {
  const {id: threadId} = await openai.beta.threads.create({
    messages: [
      { role: "user", 
        content: "Generate an exam totalling 100 marks based on the curriculum. Include Multiple Choice, short form and long form written questions. Do not answer with any confirmation of my prompt, only generate the paper. Title the paper with 'Exam - Module xxx', depending on the module. All the questions should total 100 marks; harder/ longer questions weighed higher. It is extremely important the questions you write are based entirely off the content provided in the PDF file, but do not cite any references. Give the answers AT THE END OF THE PAPER. Provide your output in Markdown formatting." // Actual prompt for GPT
      }
    ]
  });
  return threadId;
};

const runAssistant = async (threadID, assistantID) => {

  // Query GPT using the created assistant, inside the given thread. Wait for result
  // Polling - check perioidically for a result as data is not streamed back to client, but sent in one go
  const run = await openai.beta.threads.runs.createAndPoll(threadID, {
    assistant_id: assistantID,
  });

  if (run.status === "completed"){
    const response = await openai.beta.threads.messages.list(threadID); // Response contains entire GPT response context
    const messageList = response.data //  ALL messages ever sent/ received (user/ assistant) are in one long list of message objects 
    const examQuestions = messageList.filter(m => m.role === 'assistant').pop(); // Filter for the message FROM the assistant (should just be one, since each request starts a new thread) && store that message object

    const contentArray = examQuestions.content;
    const rawMarkdown = contentArray[0].text.value; // Return the content of that message object - the actual exam questions, in markdown
    return rawMarkdown
  }
};

export default{
  generateExam
};