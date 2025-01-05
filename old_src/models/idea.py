class Idea:
    def __init__(
        self,
            reddit_content_id,
            product_name,
            problem,
            solution_description,
            implementation_score,
            market_viability_score,
            differentials,
            features
    ):
        self.reddit_content_id = reddit_content_id
        self.product_name = product_name
        self.problem = problem
        self.solution_description = solution_description
        self.implementation_score = implementation_score
        self.market_viability_score = market_viability_score
        self.differentials = differentials
        self.features = features

    def to_dict(self):
        return {
            "reddit_content_id": self.reddit_content_id,
            "product_name": self.product_name,
            "problem": self.problem,
            "solution_description": self.solution_description,
            "implementation_score": self.implementation_score,
            "market_viability_score": self.market_viability_score,
            "differentials": self.differentials,
            "features": self.features,
        }
    def __repr__(self):
      return f"Idea(reddit_content_id='{self.reddit_content_id}', product_name='{self.product_name}', problem='{self.problem}', solution_description={self.solution_description}, implementation_score={self.implementation_score}, market_viability_score={self.market_viability_score}, differentials='{self.differentials}', features='{self.features}')"