describe('Test TODO system', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  let taskTitle // title of the task

  before(function () {
    // clean up by deleting the user from the database
    if (uid) {
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/users/${uid}`
      }).then((response) => {
        cy.log(response.body)
      })
    }

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
          taskTitle = response.body.title // Save task title
        })
      })
  })

  beforeEach(function () {
    // Visit the main page
    cy.visit('http://localhost:3000');

    // Log in
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email, { force: true });

    cy.get('form').submit({ force: true });
  })

  it('TC01 - Try to do to do-stuff without being logged in', () => {
    // See that user can't access todo page when not logged in
    cy.visit('http://localhost:3000'); // Visit landing page again

    cy.get('h1')
      .should('not.contain.text', 'Your tasks, ' + name)
  })

  it('TC02 - Successfully add todo to task', () => {
    // See that user can access todo page when logged in
    cy.get('h1')
      .should('contain.text', 'Your tasks, ' + name)

    cy.get('.title-overlay').click({ force: true }) // click into task
    cy.get('.inline-form > [type="text"]').type('Close video', { force: true }) // add name of todo
    cy.get('.inline-form > [type="submit"]').click({ force: true }) // submit (add) new todo to task

    // check that new todo was added to todo-list
    cy.get('.todo-list > .todo-item')
      .last() // should be last todo (bottom of list)
      .should('contain.text', 'Close video')
  })

  it('TC03 - Disabled add button when todo has no description', () => {
    cy.get('.title-overlay').click({ force: true }) // click into task

    // Ensure the input field is empty
    cy.get('.inline-form > [type="text"]').should('have.value', '')

    // Verify that the submit button is disabled
    cy.get('.inline-form > [type="submit"]').should('be.disabled')
  })

  it('TC04 - Toggle todo to done (checked)', () => {
    const todoDescription = 'Watch video';

    // navigate to task view
    cy.get('.title-overlay').click({ force: true });

    // confirm the todo exists
    cy.contains('.todo-item', todoDescription)
      .as('existingTodo');

    // click the checker to mark as done
    cy.get('@existingTodo')
      .find('.checker')
      .click({ force: true });

    // assert the todo item checker is marked as checked
    cy.get('@existingTodo')
      .find('.checker')
      .should('have.class', 'checked');

    // assert that todo text has strike throught
    cy.get('@existingTodo')
      .find('.editable')
      .should('have.css', 'text-decoration')
      .and('include', 'line-through');
  });

  it('TC05 - Untoggle todo to active (unchecked)', () => {
    const todoDescription = 'Watch video';

    // open task detailed view
    cy.get('.title-overlay').click({ force: true });

    // find the todo item
    cy.contains('.todo-item', todoDescription)
      .as('todoItem');

    // toggle to checked
    cy.get('@todoItem')
      .find('.checker')
      .click({ force: true });

    // toggle back to unchecked
    cy.get('@todoItem')
      .find('.checker')
      .click({ force: true });

    // assert the todo item checker is not marked as checked
    cy.get('@todoItem')
    .find('.checker')
    .should('not.have.class', 'checked');

    // assert that todo text has strike throught
    cy.get('@todoItem')
      .find('.editable')
      .should('have.css', 'text-decoration')
      .and((textDecoration) => {
        expect(textDecoration).not.to.include('line-through');
      });
  });


  it('TC06 - Remove todo', () => {
    const todoDescription = 'Remove this todo';

    cy.get('.title-overlay').click({ force: true }); // open task

    // add a todo that will be removed
    cy.get('.inline-form > [type="text"]').type(todoDescription, { force: true }); // Becaue of viewport i use forece: true
    cy.get('.inline-form > [type="submit"]').click({ force: true });

    // confirm it is created
    cy.contains('.todo-item', todoDescription).as('todoToDelete');

    // click the remove button
    cy.get('@todoToDelete')
      .find('.remover')
      .click({ force: true });

    // assert its no longer in the list
    cy.get('.todo-list')
      .should('not.contain.text', todoDescription);
  });


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
