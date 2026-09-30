from results import load_results


def show_leaderboard():
    results = load_results()
    print("\n=== QUIZMASTER LEADERBOARD ===")
    if not results:
        print("No results available.")
        return

    ranked = sorted(results, key=lambda r: r.get("percentage", 0), reverse=True)

    for position, result in enumerate(ranked, 1):
        print(
            f"{position}. {result['username']} - "
            f"{result['percentage']:.2f}% "
            f"({result['score']}/{result['total']})"
        )
