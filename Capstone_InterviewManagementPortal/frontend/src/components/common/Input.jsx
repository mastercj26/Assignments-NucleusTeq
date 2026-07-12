function Input({ label, name, type = 'text', value, onChange, error, hint, required, className = '', ...rest }) {
  return (
    <div className="form-group">
      {label && (
        <label className="form-label" htmlFor={name}>
          {label}
          {required && <span className="required">*</span>}
        </label>
      )}
      <input
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        className={`form-control${error ? ' has-error' : ''} ${className}`.trim()}
        {...rest}
      />
      {error && <p className="form-error">{error}</p>}
      {hint && <p className="form-hint">{hint}</p>}
    </div>
  )
}

export default Input
