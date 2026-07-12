function Textarea({ label, name, value, onChange, error, required, rows = 3, className = '', ...rest }) {
  return (
    <div className="form-group">
      {label && (
        <label className="form-label" htmlFor={name}>
          {label}
          {required && <span className="required">*</span>}
        </label>
      )}
      <textarea
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        rows={rows}
        className={`form-control${error ? ' has-error' : ''} ${className}`.trim()}
        {...rest}
      />
      {error && <p className="form-error">{error}</p>}
    </div>
  )
}

export default Textarea
