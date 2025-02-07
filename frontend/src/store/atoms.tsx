import { atom } from 'jotai'

export const usernameAtom = atom('')
export const programmingLanguageIdAtom = atom('')
export const programmingLanguagesAtom = atom([
  {
    value: '50',
    label: 'C (GCC 9.2.0)',
  },
  {
    value: '54',
    label: 'C++ (GCC 9.2.0)',
  },
  {
    value: '51',
    label: 'C# (Mono 6.6.0.161)',
  },
  {
    value: '60',
    label: 'Go (1.13.5)',
  },
  {
    value: '62',
    label: 'Java (OpenJDK 13.0.1)',
  },
  {
    value: '63',
    label: 'JavaScript (Node.js 12.14.0)',
  },
  {
    value: '67',
    label: 'Pascal (FPC 3.0.4)',
  },
  {
    value: '68',
    label: 'PHP (7.4.1)',
  },
  {
    value: '71',
    label: 'Python (3.8.1)',
  },
  {
    value: '72',
    label: 'Ruby (2.7.0)',
  },
  {
    value: '73',
    label: 'Rust (1.40.0)',
  },
  {
    value: '74',
    label: 'TypeScript (3.7.4)',
  },
])
