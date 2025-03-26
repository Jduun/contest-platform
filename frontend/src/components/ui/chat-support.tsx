import {
  ChatBubble,
  ChatBubbleAvatar,
  ChatBubbleMessage,
} from '@/components/ui/chat/chat-bubble'
import axios from 'axios'
import { ChatInput } from '@/components/ui/chat/chat-input'
import {
  ExpandableChat,
  ExpandableChatHeader,
  ExpandableChatBody,
  ExpandableChatFooter,
} from '@/components/ui/chat/expandable-chat'
import { API_URL } from '@/api'
import { ChatMessageList } from '@/components/ui/chat/chat-message-list'
import { useState, useEffect } from 'react'
import { useAtom } from 'jotai'
import { 
  botAvatarUrlAtom, 
  avatarUrlAtom, 
  programmingLanguageIdAtom, 
  programmingLanguagesAtom 
} from "@/store/atoms"
import { Problem } from '@/dto'

interface Message {
  role: string
  content: string
}

interface ChatSupportProps {
  code: string
  problem: Problem | null
}

export default function ChatSupport({code, problem}: ChatSupportProps) {
  const [programmingLanguage, setProgrammingLanguage] = useState<string | undefined>("")
  const [programmingLanguageId, _setProgrammingLanguageId] = useAtom(
    programmingLanguageIdAtom,
  )
  const [programmingLanguages, _setProgrammingLanguages] = useAtom(
    programmingLanguagesAtom,
  )
  const [messages, setMessages] = useState<Message[]>([])
  const [botAvatarUrl] = useAtom(botAvatarUrlAtom)
  const [avatarUrl] = useAtom(avatarUrlAtom)

  useEffect(() => {
    setProgrammingLanguage(
      programmingLanguages.find(
        (language) => language.value === programmingLanguageId,
      )?.label
    )
    console.log(programmingLanguage)
  }, [])

  const handleSend = (newMessage: string) => {
    const token = localStorage.getItem('token')
  
    setMessages((prevMessages) => {
      const maxChatHistoryLength = 10
      const updatedMessages = [...prevMessages, { role: 'user', content: newMessage }].slice(-maxChatHistoryLength)
  
      const getLLMAnswer = async () => {
        try {
          setProgrammingLanguage(
            programmingLanguages.find(
              (language) => language.value === programmingLanguageId,
            )?.label
          )
          const response = await axios.post(
            `${API_URL}/api/chat/generate`,
            {
              messages: updatedMessages,
              user_code: code,
              problem_statement: problem?.statement,
              programming_language: programmingLanguage,
            },
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          )
  
          const llmAnswer = response.data
          setMessages((prev) => [...prev, { role: 'assistant', content: llmAnswer }])
        } catch (err) {
          console.log(err)
        }
      }
      getLLMAnswer()
      return updatedMessages
    })
  }

  return (
    <ExpandableChat size="xl" position="bottom-right">
      <ExpandableChatHeader className="flex-col text-center justify-center">
        <h1 className="text font-semibold">AI Assistant 🤖</h1>
        <p>Bot can help you to understand the problem</p>
      </ExpandableChatHeader>
      <ExpandableChatBody>
        <ChatMessageList>
          {messages.map((message, index) => (
            <ChatBubble key={index}>
              { message.role === "assistant" ? (
                <ChatBubbleAvatar src={botAvatarUrl} />
              ) : (
                <ChatBubbleAvatar src={avatarUrl} />
              )
              }
              <ChatBubbleMessage>
                <div className="prose dark:prose-invert w-full">
                    {message.content}
                </div>
              </ChatBubbleMessage>
            
            </ChatBubble>
          ))}
        </ChatMessageList>
      </ExpandableChatBody>
      <ExpandableChatFooter>
        <ChatInput onSend={handleSend} />  
      </ExpandableChatFooter>
    </ExpandableChat>
  )
}