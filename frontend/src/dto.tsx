export interface SolvedProblemsStats {
  easy: number
  medium: number
  hard: number
}

export interface ProblemCardProps {
  id: string
  title: string
  difficulty: string
  showScore: boolean
  contest_id: string | undefined
}

export interface UserInfo {
  username: string
}

export interface Contest {
  id: string | undefined
  name: string | undefined
  start_time: string
  end_time: string
}

export interface LeaderboardEntry {
  user_id: string
  solved_count: number
  total_penalty: number
  solved_problems: string[]
  penalty_times: number[]
}

export interface User {
  id: string
  username: string
  role_id: string
  registered_at: string
}

export interface YearComboboxProps {
  startYear: number
  year: number
  setYear: React.Dispatch<React.SetStateAction<number>>
}

export interface CodeEditorProps {
  code: string
  setCode: (code: string) => void
}

export interface CalendarProps {
  activityData: any
}

export interface SubmissionListProps {
  problem_id: string
  setCode: React.Dispatch<React.SetStateAction<string>>
}

export interface Submission {
  id: string
  code: string
  problem_id: string
  language_id: number
  status: string
  submitted_at: string
}

export interface CountdownTimerProps {
  endTime: string // time in ISO format
}

export interface Problem {
  id: string
  title: string
  statement: string
  memory_limit: number
  time_limit: number
  difficulty: string
}
