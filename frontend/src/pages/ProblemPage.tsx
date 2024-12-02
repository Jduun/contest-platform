import { useParams } from "react-router"
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios, { AxiosError } from "axios";
import { Navbar } from "@/components/Navbar/Navbar";
import { CodeEditor } from "@/components/CodeEditor/CodeEditor";
import { Combobox } from "@/components/Combobox/Combobox";
import { Button } from "@/components/ui/button"
import { Loader2 } from "lucide-react"

interface Problem {
  id: string
  title: string
  statement: string
  memory_limit: number
  time_limit: number
  difficulty: string
}

export function ProblemPage() {
	const navigate = useNavigate()
	const params = useParams()
	const id = params.id
	const [problem, setProblem] = useState<Problem | null>(null)
  const [submitResponse, setSubmitResponse] = useState<string>("")
  const [code, setCode] = useState<string>("")
  const [codeProcessing, setCodeProcessing] = useState<boolean>(false)

  const difficultyToRussian: Record<string, string> = {
    easy: "Легкая",
    medium: "Средняя",
    hard: "Сложная",
  }

  useEffect(() => {
    const getProblem = async () => {
      const token = localStorage.getItem("token")
      await axios.get<Problem>(`http://localhost/api/problems/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        setProblem(response.data)
      })
      .catch((err: AxiosError) => {
        navigate("/")
      })
    }
    getProblem()
	}, [])

  const submitCode = async () => {
    setCodeProcessing(true)
    if (code == "") {
      setSubmitResponse("Напишите код")
      setCodeProcessing(false)
      return
    }
    const token = localStorage.getItem("token")
    await axios.post('http://localhost/api/submissions', 
      {
        code: code,
        problem_id: problem?.id,
        language_id: 71 
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )
    .then((response) => {      
      console.log('response data: ', response.data)
      const submissionId = response.data
      console.log('submission id: ' + submissionId)
      console.log(`Event http://localhost/api/submissions/${submissionId}`)
      const eventSource = new EventSource(`http://localhost/api/submissions/${submissionId}`);
      eventSource.onopen = () => {
        console.log('EventSource connected')
        setSubmitResponse("")
      }
      eventSource.addEventListener('locationUpdate', function (event) {
        console.log(event.data)
        const newSubmitResponse = event.data;
        console.log('LocationUpdate', newSubmitResponse);
        //setSubmitResponse(newSubmitResponse);
        setSubmitResponse(event.data)
      });
      eventSource.onerror = (error) => {
        setCodeProcessing(false)
        eventSource.close()
      }
    })
    .catch((err: AxiosError) => {
      setCodeProcessing(false)
      navigate("/")
      return
    })
  }

  return (
		<div className="flex flex-col w-full max-w-[900px] mx-auto">
			<Navbar />
      <div className="prose dark:prose-invert w-full">
        <div>
        <h1 className="m-0 text-3xl">{problem?.title}</h1>
        <p className="m-0 text-xs">
          Уровень сложности: { difficultyToRussian[problem?.difficulty || ""] }<br/>
          Ограничение по времени: {problem?.time_limit}с<br/>
          Ограничение по памяти: {problem?.memory_limit}Мб
        </p>
        </div>
        <div className="min-w-[900px]" dangerouslySetInnerHTML={{ __html: problem?.statement || "" }} />
      </div>
      <div className="flex justify-between">
        <div className="py-1">
          <Combobox />
        </div>
        <div>
          { codeProcessing ? (
            <Button disabled>
              <Loader2 className="animate-spin" />
                Подождите . . .
            </Button> ) : (
            <Button 
              type="submit" 
              className="bg-secondary"
              onClick={() => {
                submitCode()
              }}>
                Отправить решение
            </Button>
            )
          }
        </div>
      </div>
      <div className="border">
        <CodeEditor setCode={setCode}/>
      </div>
      {
        submitResponse ? (
          <p>
            Результат выполнения:
            <span
              className={`${
                submitResponse === 'Accepted'
                  ? 'text-green-500'
                  : submitResponse === 'Processing'
                  ? 'text-yellow-500'
                  : 'text-red-500'
              } mx-2 font-medium`}
            >
              {submitResponse}
            </span>
          </p>
        ) : (
          <></>
        )
      }
		</div>
  );
}
