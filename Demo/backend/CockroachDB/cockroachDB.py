import psycopg2

class CockroachDBAgent:
    def __init__(self, connection_string):
        """Initialize with a connection string"""
        self.connection_string = connection_string
        self.connection =  self.connect()
        self.cursor = None
    
    # Connects to the CockroachDB using the connection string
    def connect(self):
        """Establish a connection using the connection string"""
        try:
            self.connection = psycopg2.connect(self.connection_string)
            self.cursor = self.connection.cursor()
            print("Connected to CockroachDB successfully!")
        except Exception as e:
            print(f"Error: Unable to connect to the database: {e}")
    
    # Inserts new canidates onto the database itself
    def insert_candidate(self,first_name, last_name, description):
        """Insert a new candidate into the database"""
        try:
            self.cursor.execute(
                """
                INSERT INTO HRCandidates(description, first_name, last_name)
                VALUES (%s, %s, %s)
                """,
                (description, first_name, last_name)
            )
            self.connection.commit()
            print(f"Candidate inserted successfully!")
        except Exception as e:
            print(f"Error inserting candidate: {e}")
    
    # Retrives the new canidate information from the database
    def get_candidates(self):
        """Fetch and return all candidates from the database"""
        try:
            self.cursor.execute("SELECT * FROM HRCandidates")
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error fetching candidates: {e}")
            return []

    # Deletes the canidate information from the database 
    def delete_candidate(self, candidate_id):
        """Delete a candidate from the database by ID"""
        try:
            self.cursor.execute(
                """
                DELETE FROM HRCandidates
                WHERE id = %s
                """,
                (candidate_id,)
            )
            self.connection.commit()
            print(f"Candidate with ID {candidate_id} deleted successfully!")
        except Exception as e:
            print(f"Error deleting candidate: {e}")
            
    def print_candidates(self):
        """Print the candidate data fetched from the database"""
        rows = self.get_candidates()
        for count, row in enumerate(rows):
            print("Canidate: ", count, "Information: ", row)
    
    def close(self):
        """Close the connection to the database"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed.")
        
    def as_retriver(self): 
        return self


    
# if __name__ == "__main__":
    # For This I need to hardcode the connection string and manually test all the functions before to build my rest API
#     connection_string = ""
#     db_agent = CockroachDBAgent(connection_string)
    
#     db_agent.connect()
#     # db_agent.insert_candidate("This is a long description of the candidate.")
    
#     # Print all candidates
#     db_agent.print_candidates()

#     # db_agent.clear_candidates()
    
#     # Close the connection
#     db_agent.close()