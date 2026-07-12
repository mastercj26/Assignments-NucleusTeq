function Select({ label, name, value, onChange, error, hint, required, children, className = '', ...rest }) {
  return (
    <div className="form-group">
      {label && (
        <label className="form-label" htmlFor={name}>
          {label}
          {required && <span className="required">*</span>}
        </label>
      )}
      <select
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        className={`form-control${error ? ' has-error' : ''} ${className}`.trim()}
        {...rest}
      >
        {children}
      </select>
      {error && <p className="form-error">{error}</p>}
      {hint && <p className="form-hint">{hint}</p>}
    </div>
  )
}

export default Select
