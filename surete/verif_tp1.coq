Proposition modus_ponens :
forall A B : Prop, (A -> B) -> A -> B.

Proof.
  intros.
  apply H.
  apply H0.
Qed.



Proposition modus_ponens :
forall A B C : Prop, (A -> B) /\ (B -> C) -> A -> C.

Proof.
  intros.
  apply H.
  apply H.
  apply H0.
Qed.

Proposition modus_ponens :
forall A B : Prop, (A -> B) -> ~B -> ~A.

Proof.
  intros.
  intro .
  apply H0.
  apply H.
  apply H1.
Qed.


Proposition a_or_b_false_left:
forall A B : Prop, (( A \/ B) -> False) -> (A -> False).

Proof.
  intros.
  apply H.
  left .
  apply H0.
Qed.


Proposition a_or_b_false_right:
forall A B : Prop, (( A \/ B) -> False) -> (B -> False).

Proof.
  intros.
  apply H.
  right .
  apply H0.
Qed.




Proposition de_morgan_bool_1 :
forall a b:bool, negb (orb a b) = andb (negb a) (negb b).

Proof.
  intros.
  destruct a.
  destruct b.
  reflexivity.
  reflexivity.
  reflexivity.
Qed.


Proposition de_morgan_bool_2 :
forall a b:bool, negb (andb a b) = orb (negb a) (negb b).

Proof.
  intros.
  destruct a.
  destruct b.
  reflexivity.
  reflexivity.
  reflexivity.
Qed.


Proposition de_morgan_1 :
forall P Q, ~(P \/ Q) -> ~P /\ ~Q.

Proof.
  intros.
  split .
  intro.
  apply H.
  left.
  apply H0.
  intro.
  apply H.
  right.
  apply H0.
Qed.


Proposition de_morgan_2 :
forall P Q, ~P /\ ~Q -> ~(P \/ Q).

Proof.
  intros.
  intro.
  destruct H.
  destruct H0.
  apply H.
  apply H0.
  apply H1.
  apply H0.
Qed.


Proposition de_morgan_1_2 :
forall P Q, ~P /\ ~Q <-> ~(P \/ Q).

Proof.
  intros.
  split.
  intro.
  intro.
  destruct H.
  destruct H0.
  apply H.
  apply H0.
  apply H1.
  apply H0.
  intro.
  split.
  intro.
  apply H.
  left.
  apply H0.
  intro.
  apply H.
  right.
  apply H0.
Qed.

