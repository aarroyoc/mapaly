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
      cy.get('#question').then(x => {
        let question = x.text();
        if(question === "Burgos"){
          cy.get('[d="M409 80L413 80L411 83L413 84L413 87L411 89L417 90L417 92L420 94L419 96L415 97L409 93L406 97L409 101L411 98L412 99L414 97L415 98L412 102L414 104L413 105L417 105L418 107L423 108L426 113L416 113L413 119L415 119L417 125L417 129L416 126L414 126L414 128L417 130L414 131L414 140L418 147L422 147L423 150L419 159L415 160L412 164L407 159L407 166L403 169L399 176L394 177L395 178L390 178L386 181L387 184L384 185L385 180L383 181L382 184L373 175L373 171L371 169L372 164L370 160L375 158L375 156L378 155L379 152L373 155L375 149L370 150L369 148L371 146L365 144L361 130L359 129L360 124L362 124L363 122L360 118L362 114L361 111L367 106L368 107L376 105L379 102L380 104L382 102L382 98L380 97L379 100L378 98L379 96L380 97L382 95L380 93L379 95L375 96L375 92L383 85L385 85L390 79L396 82L401 82L408 78L409 79zM370 142L369 143L371 144L371 142zM427 103L440 105L437 109L439 111L440 110L441 112L440 113L433 110L430 111L425 106L426 105z"]').click();
        }else{
          cy.get('[d="M450 143L452 144L453 147L459 146L458 148L460 154L466 157L472 154L472 164L475 169L474 173L471 173L468 177L465 176L467 187L464 190L463 187L460 186L460 190L457 193L458 202L463 204L462 208L455 207L453 209L447 209L438 203L438 199L426 196L425 193L417 196L409 194L404 190L404 185L402 185L399 180L395 180L394 177L398 177L403 169L407 167L407 159L412 165L415 160L419 159L423 151L429 149L428 147L430 144L432 144L433 146L430 150L438 152L442 148L442 145L449 143z"]').click();
        }
        cy.wait(1000);
        cy.get('#question').then(y =>{
          expect(question).to.not.equal(y.text());
        });
      });
    });

    it("when I click on a correct province, score goes up", ()=>{
      cy.visit("http://nginx:1133/");
      cy.contains('Provincias de España').click();
      cy.get('#question').then(q=>{
        const question = q.text();
        cy.get('#points').then(q => {
          const score = Number(q.text());
          if(question === "Burgos"){
            cy.get('[d="M409 80L413 80L411 83L413 84L413 87L411 89L417 90L417 92L420 94L419 96L415 97L409 93L406 97L409 101L411 98L412 99L414 97L415 98L412 102L414 104L413 105L417 105L418 107L423 108L426 113L416 113L413 119L415 119L417 125L417 129L416 126L414 126L414 128L417 130L414 131L414 140L418 147L422 147L423 150L419 159L415 160L412 164L407 159L407 166L403 169L399 176L394 177L395 178L390 178L386 181L387 184L384 185L385 180L383 181L382 184L373 175L373 171L371 169L372 164L370 160L375 158L375 156L378 155L379 152L373 155L375 149L370 150L369 148L371 146L365 144L361 130L359 129L360 124L362 124L363 122L360 118L362 114L361 111L367 106L368 107L376 105L379 102L380 104L382 102L382 98L380 97L379 100L378 98L379 96L380 97L382 95L380 93L379 95L375 96L375 92L383 85L385 85L390 79L396 82L401 82L408 78L409 79zM370 142L369 143L371 144L371 142zM427 103L440 105L437 109L439 111L440 110L441 112L440 113L433 110L430 111L425 106L426 105z"]').click();
          }else{
            cy.get('[d="M450 143L452 144L453 147L459 146L458 148L460 154L466 157L472 154L472 164L475 169L474 173L471 173L468 177L465 176L467 187L464 190L463 187L460 186L460 190L457 193L458 202L463 204L462 208L455 207L453 209L447 209L438 203L438 199L426 196L425 193L417 196L409 194L404 190L404 185L402 185L399 180L395 180L394 177L398 177L403 169L407 167L407 159L412 165L415 160L419 159L423 151L429 149L428 147L430 144L432 144L433 146L430 150L438 152L442 148L442 145L449 143z"]').click();
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
        cy.get('[d="M209 43L210 49L213 44L219 47L227 55L236 56L235 61L229 64L229 66L240 82L243 81L243 79L245 80L243 85L240 85L238 89L239 91L240 88L240 90L245 93L244 96L246 98L243 98L245 101L243 104L235 109L237 112L235 115L235 119L228 132L225 127L219 125L215 128L210 128L198 121L195 116L198 109L193 104L192 99L196 95L194 72L197 70L197 66L200 65L204 57L203 54L206 48L206 44L209 43z"]').click();
        cy.get('#points').then(y => {
          const newScore = Number(y.text());
          expect(newScore).to.be.lessThan(score);
        });
      });
    });

    it("when I click on an incorrect province, question doesn't change", ()=>{
      cy.get('#question').then(x=>{
        const question = x.text();
        cy.get('[d="M209 43L210 49L213 44L219 47L227 55L236 56L235 61L229 64L229 66L240 82L243 81L243 79L245 80L243 85L240 85L238 89L239 91L240 88L240 90L245 93L244 96L246 98L243 98L245 101L243 104L235 109L237 112L235 115L235 119L228 132L225 127L219 125L215 128L210 128L198 121L195 116L198 109L193 104L192 99L196 95L194 72L197 70L197 66L200 65L204 57L203 54L206 48L206 44L209 43z"]').click();
        cy.get('#question').should("contain", question);
      });
    });
});
