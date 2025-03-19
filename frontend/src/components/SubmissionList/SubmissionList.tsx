import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { useAtom } from 'jotai'
import { programmingLanguagesAtom } from '@/store/atoms'
import axios, { AxiosError } from 'axios'
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Submission, SubmissionListProps } from '@/dto'
import { API_URL } from '@/api'

const formatDate = (isoString: string): string => {
  const date = new Date(isoString)
  const formattedDate = date.toISOString().split('T')[0]
  const formattedTime = date.toTimeString().slice(0, 5)
  return `${formattedDate}, ${formattedTime}`
}

export function SubmissionList({ problem_id, setCode }: SubmissionListProps) {
  const [lastSubmissions, setLastSubmissions] = useState<Submission[]>([])
  const [programmingLanguages, _setProgrammingLanguages] = useAtom(
    programmingLanguagesAtom,
  )
  const navigate = useNavigate()

  useEffect(() => {
    const getLastSubmissions = async () => {
      const token = localStorage.getItem('token')
      await axios
        .get<Submission[]>(`${API_URL}/api/submissions/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          params: {
            problem_id: problem_id,
            offset: 0,
            limit: 10,
          },
        })
        .then((response) => {
          setLastSubmissions(response.data)
        })
        .catch((err: AxiosError) => {
          console.log(err)
          navigate('/')
        })
    }
    getLastSubmissions()
  }, [])

  return (
    <>
      {lastSubmissions.length !== 0 ? (
        <>
          <p className="text-xl font-bold">Last Submissions</p>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="font-bold">Status</TableHead>
                <TableHead className="font-bold">Language</TableHead>
                <TableHead className="text-right font-bold">
                  Submitted at
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {lastSubmissions.map((submission) => (
                <TableRow
                  key={submission.id}
                  className={`${
                    submission.status === 'Accepted'
                      ? 'text-green-500'
                      : submission.status === 'Processing'
                        ? 'text-yellow-500'
                        : 'text-red-500'
                  } font-bold cursor-pointer`}
                  onClick={() => {
                    console.log('click')
                    setCode(submission.code)
                    console.log(submission.code)
                  }}
                >
                  <TableCell>{submission.status}</TableCell>
                  <TableCell>
                    {
                      programmingLanguages.find(
                        (item: any) => item.value == submission.language_id,
                      )?.label
                    }
                  </TableCell>
                  <TableCell className="text-right">
                    {formatDate(submission.submitted_at)}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </>
      ) : (
        <></>
      )}
    </>
  )
}
