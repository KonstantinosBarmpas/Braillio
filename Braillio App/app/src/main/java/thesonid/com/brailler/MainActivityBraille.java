package thesonid.com.brailler;

/**
 * Created by Konstantinos Barmpas.
 */

import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class MainActivityBraille extends AppCompatActivity {

    //Declare Activity variables.

    private Button LogIn, SetUp, ChangePassword;
    private EditText passwordedit, boardedit;
    private Context context;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        context = this;
        setContentView(R.layout.activity_main_brailler);

        //Set the EditText areas and buttons of the layout.

        boardedit = (EditText) findViewById(R.id.board_number);
        passwordedit = (EditText) findViewById(R.id.board_password);
        LogIn = (Button) findViewById(R.id.log_in);
        SetUp = (Button) findViewById(R.id.set_up);
        ChangePassword = (Button) findViewById(R.id.password_change);

        //When clicked starts the MainActivity activity.

        SetUp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivityBraille.this, MainActivity.class);
                startActivity(intent);
            }

        });

        //When clicked starts the Passwordchange activity.

        ChangePassword.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivityBraille.this, Passwordchange.class);
                startActivity(intent);
            }

        });

        //When clicked communicates with the database.

        LogIn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                /*Gets the data from the TextEdit fields. Does the neccesary data validation.
                 Connects to the database.
                 If the input password and board number match with a pair of the database then
                 the WordActivity starts with the data of that user. Otherwise it shows an error message.
                */

                //Data get and validation
                final String password = passwordedit.getText().toString().trim();
                final String board = boardedit.getText().toString().trim();

                final DatabaseReference mDatabase;
                mDatabase = FirebaseDatabase.getInstance().getReference();
                DatabaseReference boards = mDatabase.child("Boards");

                if (TextUtils.isEmpty(password)) {
                    Toast.makeText(getApplicationContext(), "Please enter password", Toast.LENGTH_SHORT).show();
                    return;
                }
                if (TextUtils.isEmpty(board)) {
                    Toast.makeText(getApplicationContext(), "Please enter board number", Toast.LENGTH_SHORT).show();
                    return;
                }

                passwordedit.setText("");
                boardedit.setText("");

                //Communication with the database
                DatabaseReference boardref = boards.child(board).child("password");
                boardref.addListenerForSingleValueEvent(new ValueEventListener() {
                    @Override
                    public void onDataChange(DataSnapshot snapshot) {
                        if (snapshot.hasChild(password)) {
                            Intent intent = new Intent(MainActivityBraille.this, WordActivity.class);
                            intent.putExtra("board", board);
                            startActivity(intent);
                        } else {
                            Toast.makeText(context, "Wrong password-board combination", Toast.LENGTH_LONG).show();
                        }
                    }

                    @Override
                    public void onCancelled(DatabaseError databaseError) {
                    }
                });
            }
        });

    }


}
