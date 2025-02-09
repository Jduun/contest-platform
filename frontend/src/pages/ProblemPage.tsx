import { useParams } from 'react-router'
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios, { AxiosError } from 'axios'
import { Navbar } from '@/components/Navbar/Navbar'
import { CodeEditor } from '@/components/CodeEditor/CodeEditor'
import { Combobox } from '@/components/Combobox/Combobox'
import { Button } from '@/components/ui/button'
import { Loader2 } from 'lucide-react'
import { useAtom } from 'jotai'
import { programmingLanguageIdAtom } from '@/store/atoms'

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
  const problem_id = params.problem_id
  const contest_id = params.contest_id
  const [problem, setProblem] = useState<Problem | null>(null)
  const [submissionStatus, setSubmissionStatus] = useState<string>('')
  const [code, setCode] = useState<string>('')
  const [codeProcessing, setCodeProcessing] = useState<boolean>(false)
  const [programmingLanguageId, _setProgrammingLanguageId] = useAtom(programmingLanguageIdAtom)

  const difficultyToRussian: Record<string, string> = {
    easy: 'Легкая',
    medium: 'Средняя',
    hard: 'Сложная',
  }

  useEffect(() => {
    const getProblem = async () => {
      const token = localStorage.getItem('token')
      await axios
        .get<Problem>(`http://localhost/api/problems/${problem_id}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          setProblem(response.data)
        })
        .catch((_err: AxiosError) => {
          navigate('/')
        })
    }
    getProblem()
  }, [])

  const submitCode = async () => {
    setCodeProcessing(true)
    if (code == '') {
      setSubmissionStatus('Напишите код')
      setCodeProcessing(false)
      return
    }
    const token = localStorage.getItem('token')
    await axios
      .post(
        'http://localhost/api/submissions',
        {
          code: code,
          problem_id: problem?.id,
          language_id: programmingLanguageId,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      )
      .then((response) => {
        console.log('response data: ', response.data)
        const submissionId = response.data
        console.log('submission id: ' + submissionId)
        console.log(`Event http://localhost/api/submissions/${submissionId}`)
        let submission_status = ''
        const eventSource = new EventSource(
          `http://localhost/api/submissions/${submissionId}`,
        )
        eventSource.onopen = () => {
          console.log('EventSource connected')
          setSubmissionStatus('')
        }
        eventSource.addEventListener('locationUpdate', function (event) {
          setSubmissionStatus(event.data)
          submission_status = event.data
        })
        eventSource.onerror = (_error) => {
          eventSource.close()
          setCodeProcessing(false)
          if (contest_id !== undefined) {
            setPenaltyTime(submission_status)
          }
        }
      })
      .catch((_err: AxiosError) => {
        setCodeProcessing(false)
        navigate('/')
        return
      })
  }

  const setPenaltyTime = async (status: string) => {
    const token = localStorage.getItem('token')
    await axios.post(
      `http://localhost/api/contests/${contest_id}/problems/${problem_id}/set-penalty-time`,
      {
        status: status,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )
  }

  return (
    <div className="flex flex-col w-full max-w-[900px] mx-auto">
      <Navbar />
      {
      //<>Контест: {contest_id}</>
      //<>Задача: {problem_id}</>
      }
      <div className="prose dark:prose-invert w-full">
        <div>
          <h1 className="m-0 text-3xl">{problem?.title}</h1>
          <p className="m-0 text-xs">
            Уровень сложности: {difficultyToRussian[problem?.difficulty || '']}
            <br />
            Ограничение по времени: {problem?.time_limit}с<br />
            Ограничение по памяти: {problem?.memory_limit}Мб
          </p>
        </div>
        <div
          className="min-w-[900px]"
          dangerouslySetInnerHTML={{ __html: problem?.statement || '' }}
        />
      </div>
      <div className="flex justify-between">
        <div className="py-1">
          <Combobox />
        </div>
        <div>
          {codeProcessing ? (
            <Button disabled>
              <Loader2 className="animate-spin" />
              Подождите . . .
            </Button>
          ) : (
            <Button
              type="submit"
              className="bg-secondary"
              onClick={() => {
                submitCode()
              }}
            >
              Отправить решение
            </Button>
          )}
        </div>
      </div>
      <div className="border">
        <CodeEditor setCode={setCode} />
      </div>
      {submissionStatus ? (
        <p>
          Результат выполнения:
          <span
            className={`${
              submissionStatus === 'Accepted'
                ? 'text-green-500'
                : submissionStatus === 'Processing'
                  ? 'text-yellow-500'
                  : 'text-red-500'
            } mx-2 font-medium`}
          >
            {submissionStatus}
          </span>
        </p>
      ) : (
        <></>
      )}
    </div>
  )
}
