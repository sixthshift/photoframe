import 'bootstrap/dist/css/bootstrap.min.css'
import React from 'react'
import { Col, Container, Row } from 'react-bootstrap'

import PhotoProvider from './photos'

import Actions from './actions'
import Gallery from './gallery'

export default function App () {
  return (
    <PhotoProvider>
      <Container className='py-4'>
        <Row className='mb-3'>
          <Col>
            <Actions />
          </Col>
        </Row>
        <Row>
          <Col>
            <Gallery />
          </Col>
        </Row>
      </Container>
    </PhotoProvider>
  )
}
