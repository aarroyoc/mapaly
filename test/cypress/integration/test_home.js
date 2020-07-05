describe('Home Page', () => {
    it('shows maps', () => {
      cy.visit("http://127.0.0.1:1133/");

      cy.contains('Provincias de España');
    });

    it("when I click I go to quiz page", () => {
      cy.visit("http://127.0.0.1:1133/");
      cy.contains('Provincias de España').click();

      cy.url().should("include", "quiz");
    });

});
