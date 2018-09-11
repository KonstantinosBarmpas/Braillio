package thesonid.com.brailler;

/**
 * Created by Konstantinos Barmpas.
 */

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.text.TextUtils;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.firebase.ui.database.FirebaseRecyclerAdapter;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class WordActivity extends AppCompatActivity {

    //Declare Activity variables.

    private static RecyclerView mRecyclerView;
    private static FirebaseRecyclerAdapter mFirebaseAdapter;
    private static DatabaseReference mReference;
    private String id;
    private EditText wordedit;
    private Button add;
    private ValueEventListener mListener;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.word_layout);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        //Set the variables, EditText areas and buttons of the layout.

        Intent intent = getIntent();
        id = intent.getStringExtra("board");
        final FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference zonesRef = database.getInstance().getReference("Boards");
        DatabaseReference zone1Ref = zonesRef.child(id);
        mReference = zone1Ref.child("words");
        wordedit = (EditText) findViewById(R.id.word);
        add = (Button) findViewById(R.id.add_word);
        mRecyclerView = (RecyclerView) findViewById(R.id.recycler_view);
        LinearLayoutManager layoutManager = new LinearLayoutManager(this);
        mRecyclerView.setLayoutManager(layoutManager);
        mRecyclerView.setHasFixedSize(true);
        mRecyclerView.setLayoutManager(layoutManager);

        //Validation and add new word to the database.

        add.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String word = wordedit.getText().toString().trim();
                if (TextUtils.isEmpty(word)) {
                    Toast.makeText(getApplicationContext(), "Please enter a valid word", Toast.LENGTH_SHORT).show();
                    return;
                }
                if (word.length() > 4) {
                    Toast.makeText(getApplicationContext(), "This word is more than 4 letters", Toast.LENGTH_SHORT).show();
                    return;
                }
                mReference.child(word).setValue(word);
                wordedit.setText("");
            }
        });

        //Listener to database changes.

        mReference.addValueEventListener(mListener = new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                setUpFirebaseAdapter(id);
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {
            }
        });
        setUpFirebaseAdapter(id);
    }


    //Populate recycler view.

    static public void setUpFirebaseAdapter(String id) {
        FirebaseWordsViewHolder.createVector();
        FirebaseWordsViewHolder.getRef(id);
        mFirebaseAdapter = new FirebaseRecyclerAdapter<String, FirebaseWordsViewHolder>
                (String.class, R.layout.word_card, FirebaseWordsViewHolder.class,
                        mReference) {
            @Override
            protected void populateViewHolder(FirebaseWordsViewHolder viewHolder,
                                              String model, int position) {
                viewHolder.bindData(model);
            }
        };
        mRecyclerView.setAdapter(mFirebaseAdapter);
    }

    //On destroy of the activity stop database listeners.

    @Override
    protected void onDestroy() {
        super.onDestroy();
        mReference.removeEventListener(mListener);
        mFirebaseAdapter.cleanup();
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case android.R.id.home:
                finish();
                return true;
            default:
                return super.onOptionsItemSelected(item);

        }
    }


}
