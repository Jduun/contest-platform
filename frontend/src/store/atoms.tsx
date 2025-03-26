import { atom } from 'jotai'
import { Problem } from '@/dto';

interface ProblemsState {
  [key: number]: Problem[]
}

export const usernameAtom = atom('')
export const botAvatarUrlAtom = atom('https://img.freepik.com/free-vector/chatbot-chat-message-vectorart_78370-4104.jpg')
export const avatarUrlAtom = atom('')
export const activityDataAtom = atom([])

export const problemsAtom = atom<ProblemsState>({})
export const programmingLanguageIdAtom = atom('')
export const programmingLanguagesAtom = atom([
  {
    value: '50',
    label: 'C (GCC 9.2.0)',
    mode: 'c_cpp',
  },
  {
    value: '54',
    label: 'C++ (GCC 9.2.0)',
    mode: 'c_cpp',
  },
  {
    value: '51',
    label: 'C# (Mono 6.6.0.161)',
    mode: 'csharp',
  },
  {
    value: '60',
    label: 'Go (1.13.5)',
    mode: 'golang',
  },
  {
    value: '62',
    label: 'Java (OpenJDK 13.0.1)',
    mode: 'java',
  },
  {
    value: '67',
    label: 'Pascal (FPC 3.0.4)',
    mode: 'pascal',
  },
  {
    value: '71',
    label: 'Python (3.8.1)',
    mode: 'python',
  },
  {
    value: '73',
    label: 'Rust (1.40.0)',
    mode: 'rust',
  },
  {
    value: '74',
    label: 'TypeScript (3.7.4)',
    mode: 'typescript',
  },
])
