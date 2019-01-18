import React from 'react'

const TableHeader = (props) => {
  return (
    <div
      className="card-header d-flex align-items-baseline justify-content-between"
      style={{backgroundColor: '#fff'}}
    >
      {props.children}
    </div>
  )
}

export default TableHeader
