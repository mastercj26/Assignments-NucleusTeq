import { useState } from 'react'

function TagInput({ label, value = [], onChange, error, required, placeholder = 'Type and press Enter or Add' }) {
  const [input, setInput] = useState('')

  const addTag = () => {
    const trimmed = input.trim()
    if (trimmed && !value.includes(trimmed)) {
      onChange([...value, trimmed])
    }
    setInput('')
  }

  const removeTag = (tag) => {
    onChange(value.filter((t) => t !== tag))
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      addTag()
    }
  }

  return (
    <div className="form-group">
      {label && (
        <label className="form-label">
          {label}
          {required && <span className="required">*</span>}
        </label>
      )}
      <div className="tag-input-row">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          className={`form-control${error ? ' has-error' : ''}`}
          placeholder={placeholder}
        />
        <button type="button" className="btn btn-secondary" onClick={addTag}>
          Add
        </button>
      </div>
      {value.length > 0 && (
        <div className="tags">
          {value.map((tag) => (
            <span key={tag} className="tag">
              {tag}
              <button type="button" className="tag-remove" onClick={() => removeTag(tag)}>
                &times;
              </button>
            </span>
          ))}
        </div>
      )}
      {error && <p className="form-error">{error}</p>}
    </div>
  )
}

export default TagInput
