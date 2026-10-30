export default function Learning() {
  return (
    <section className="panel prose">
      <h2>Learn through the project</h2>
      <h3>Relationships preserve meaning</h3>
      <p>
        A prediction stores a game identifier, rather than copying a team name.
        This foreign key lets the database reject predictions that refer to
        nonexistent fixtures.
      </p>
      <h3>Locked forecasts and separate results</h3>
      <p>
        The prediction records what was known before the game. Settlement
        records what happened afterwards. Keeping these separate protects our
        research from hindsight.
      </p>
      <h3>Paper return</h3>
      <p>
        A winning one-unit selection at decimal odds 1.90 returns 0.90 units of
        profit. A loss is −1 unit. Pushes and voids return the stake, so profit
        is zero.
      </p>
      <p>
        Exercise: change a synthetic selection threshold, record a new
        prediction, and compare the outcomes. Never edit an old locked
        prediction.
      </p>
      <p>
        See docs/learning-guide.md for the code map, tests and further
        exercises.
      </p>
    </section>
  );
}
