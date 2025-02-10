import { useRef, useState } from 'react'
import axios from 'axios'
import { Button } from '@/components/ui/button'
import { Pencil } from 'lucide-react'

const uploadAvatar = async (file: File) => {
  const formData = new FormData()
  formData.append('avatar', file)
  const token = localStorage.getItem('token')

  await axios.post('http://localhost/api/users/avatars', formData, {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'multipart/form-data',
    },
  })
}

export function UploadAvatar() {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [loading, setLoading] = useState(false)

  const handleFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    if (event.target.files && event.target.files.length > 0) {
      setLoading(true)
      await uploadAvatar(event.target.files[0])
      setLoading(false)
      window.location.reload()
    }
  }

  return (
    <div className="flex flex-col items-center py-2">
      <input
        type="file"
        accept="image/png, image/jpeg, image/gif"
        className="hidden"
        ref={fileInputRef}
        onChange={handleFileChange}
      />

      <Button
        onClick={() => fileInputRef.current?.click()}
        disabled={loading}
        className="flex items-center gap-2"
      >
        <Pencil size={14} />
        {loading ? 'Uploading...' : 'Edit Avatar'}
      </Button>
    </div>
  )
}
