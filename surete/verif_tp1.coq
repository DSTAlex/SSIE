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

Proposition plus_n_0 :
forall n: nat, n+0=n.

Proof.
  intros.
  
  induction n.
    simpl.
    reflexivity.
    simpl.
    rewrite IHn.
    reflexivity.
Qed.

Proposition double_is_plus:
forall n : nat, n+n=2*n.

Proof.
  intros.
  induction n.
  simpl.
  reflexivity.
  simpl.
  rewrite plus_n_0.
  reflexivity.
Qed.

Fixpoint fact (n:nat) : nat :=
match n with
| 0 => 1
| S n' => n * fact n' end.


Fixpoint even (n:nat) : Prop :=
match n with
| 0 => True
| S 0 => False
| S (S k) => even k 
end.




Proposition add_succ_l :
forall n m: nat, S n + m = S (n + m).

Proof.
  intros.
  simpl.
  reflexivity.
Qed.

Proposition add_succ_r :
forall n m: nat, n + S m = S (n + m).

Proof.
  intros.
  induction n.
  simpl.
  reflexivity.
  simpl.
  rewrite IHn.
  reflexivity.
Qed.

Proposition one_of_two_succ_is_even:
forall n : nat, (even n) \/ (even (S n)).

Proof.
  intros.
  induction n.
  left.
  simpl.
  reflexivity.
  destruct IHn.
  simpl.
  right.
  apply H.
  left.
  apply H.  
Qed.

Proposition but_not_both :
forall n : nat, even n -> ~ (even (S n)).

Proof.
    intros.
    induction n.
    simpl.
    intro.
    apply H0.
    
    simpl.
    intro.
    apply IHn.
    apply H0.
    apply H.
Qed.



Proposition double_is_even :
forall n : nat, even (n*2).

Proof.
  intros.
  induction n.
  simpl.
  reflexivity.
  simpl.
  apply IHn.
Qed.



Proposition succ_double_is_odd :
forall n : nat, ~(even (S (n*2))).

Proof.
  intros.
  apply but_not_both.
  apply double_is_even.
Qed.


Proposition pair_induction :
forall (P : nat -> Prop),
P 0 -> P 1 -> (forall n, P n -> P (S n) -> P (S (S n))) ->
forall x, P x.

Proof.
  intros.
  assert ((P x) /\ (P (S x))).
  induction x.
  split.
  apply H.
  apply H0.
  destruct IHx.
  split.
  apply H3.
  apply H1.
  apply H2.
  apply H3.
  destruct H2.
  apply H2.  
Qed.





Proposition even_sum :
forall n m : nat, even (n) /\ even (m) -> even ( n + m ).

Proof.
  intros.  
  induction m using pair_induction.
  rewrite plus_n_0.
  destruct H.
  apply H.
  destruct H.
  rewrite add_succ_r.
  rewrite plus_n_0.
  simpl in H0.
  contradiction.
  
  rewrite add_succ_r.
  rewrite add_succ_r.
  simpl.
  apply IHm.
  simpl in H.
  apply H.
Qed.



