describe('Test TODO system', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  let taskTitle // title of the task

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
      .type(email);

    cy.get('form').submit();
  })

  it('TC01 - Try to do to do-stuff without being logged in', () => {
    // See that user can't access todo page when not logged in
    cy.clearCookies(); // Clear cookies (to remove login)
    cy.visit('http://localhost:3000'); // Visit landing page again

    cy.get('h1')
      .should('not.contain.text', 'Your tasks, ' + name)
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

  it('TC03 - Disabled add button when todo has no description', () => {
    cy.get('.title-overlay').click() // click into task

    // Ensure the input field is empty
    cy.get('.inline-form > [type="text"]').should('have.value', '')

    // Verify that the submit button is disabled
    cy.get('.inline-form > [type="submit"]').should('be.disabled')
  })

  it('TC04 - Toggle todo to done (checked)', () => {
    const todoDescription = 'Watch video';

    cy.get('.title-overlay').click(); // Navigate to task view

    // confirm the todo exists
    cy.contains('.todo-item', todoDescription)
      .as('existingTodo');

    // click the checker to mark as done
    cy.get('@existingTodo')
      .find('.checker')
      .click();

    // assert the todo item is marked as checked
    cy.get('@existingTodo')
      .should('have.class', 'checked');
  });

  it('TC05 - Untoggle todo to active (unchecked)', () => {
    const todoDescription = 'Watch video';

    cy.get('.title-overlay').click(); // open task

    // find and toggle to "checked"
    cy.contains('.todo-item', todoDescription)
      .as('todoItem');

    cy.get('@todoItem')
      .find('.checker')
      .click();

    // toggle back to unchecked
    cy.get('@todoItem')
      .find('.checker')
      .click();

    // assert it no longer has the uncheced class
    cy.get('@todoItem')
      .should('not.have.class', 'unchecked');
  });


  it('TC06 - Remove todo', () => {
    const todoDescription = 'Remove this todo';

    cy.get('.title-overlay').click(); // open task

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
