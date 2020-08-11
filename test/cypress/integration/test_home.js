describe('Home Page', () => {
    it('shows maps', () => {
      cy.visit("http://nginx:1133/");

      cy.contains('Provincias de España');
    });

    it("when I click I go to quiz page", () => {
      cy.visit("http://nginx:1133/");
      cy.contains('Provincias de España').click();

      cy.url().should("include", "quiz");
    });

    it("when I wait, time passes", () => {
      cy.visit("http://nginx:1133/");
      cy.contains('Provincias de España').click();
      cy.get('#time-string').contains("0:00");
      cy.wait(1000);
      cy.get("#time-string").contains("0:01");

    });

    it("when I click on a correct province, question changes", ()=>{
      cy.visit("http://nginx:1133/");
      cy.contains('Provincias de España').click();
      cy.wait(1000);
      cy.get('#question').then(x => {
        let question = x.text();
        if(question === "Burgos"){
          cy.get("#map").click(400, 100); // Burgos
        }else{
          cy.get("#map").click(450, 200); // Soria
        }
        
        cy.wait(1000);
        cy.get('#question').should(y =>{
          expect(y).to.not.contain(question);
        });
      });
    });

    it("when I click on a correct province, score goes up", ()=>{
      cy.visit("http://nginx:1133/");
      cy.contains('Provincias de España').click();
      cy.wait(1000);
      cy.get('#question').then(q=>{
        const question = q.text();
        cy.get('#points').then(q => {
          const score = Number(q.text());
          if(question === "Burgos"){
            cy.get("#map").click(400, 100); // Burgos
          }else{
            cy.get("#map").click(450, 200); // Soria
          }
          cy.wait(1000);
          cy.get('#points').then(q =>{
            const newScore = Number(q.text());
            expect(newScore).to.be.greaterThan(score);
          });
        });
      });
    });

    it("when I click on an incorrect province, score decreases", ()=>{
      cy.get('#points').then(x=>{
        const score = Number(x.text());
        cy.get('#map').click(160,100);
        cy.get('#points').then(y => {
          const newScore = Number(y.text());
          expect(newScore).to.be.lessThan(score);
        });
      });
    });

    it("when I click on an incorrect province, question doesn't change", ()=>{
      cy.get('#question').then(x=>{
        const question = x.text();
        cy.get('#map').click(160, 100);
        cy.get('#question').should("contain", question);
      });
    });
});
