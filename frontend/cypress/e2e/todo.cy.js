describe('Test TODO system', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  before(function () {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          email = user.email
        })
      })

    // create task
    cy.fixture('task.json')
      .then((task) => {

        // add userid from created user
        task.userid = uid;

        // add task to user account
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/tasks/create',
          form: true,
          body: task
        }).then((response) => {
          console.log(response);
        })
      })
    })

  beforeEach(function () {
    // enter the main main page
    cy.visit('http://localhost:3000')

    // detect a div which contains "Email Address", find the input and type (in a declarative way)
    cy.contains('div', 'Email Address')
    .find('input[type=text]')
    .type(email)

  // submit the form on this page
  cy.get('form')
    .submit()
  })

  it('access todo page when logged in', () => {
    // See that user can access todo page when logged in
    cy.get('h1')
      .should('contain.text', 'Your tasks, ' + name)
  })

  it('TC02 - Successfully add todo to task', () => {
    // See that user can access todo page when logged in
    cy.get('h1')
      .should('contain.text', 'Your tasks, ' + name)

    cy.get('.title-overlay').click() // click into task
    cy.get('.inline-form > [type="text"]').type('Close video') // add name of todo
    cy.get('.inline-form > [type="submit"]').click() // submit (add) new todo to task

    // check that new todo was added to todo-list
    cy.get('.todo-list > .todo-item')
      .last() // should be last todo (bottom of list)
      .should('contain.text', 'Close video')
  })

  after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})
